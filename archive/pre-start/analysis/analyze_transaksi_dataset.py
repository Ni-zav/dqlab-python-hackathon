from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT.parent / "dataset" / "Transaksi.csv"
REPORT_PATH = ROOT / "dataset_deep_dive.md"
DAILY_REVENUE_CHART = ROOT / "dataset_daily_revenue.png"
WEEKDAY_REVENUE_CHART = ROOT / "dataset_weekday_revenue.png"
TOP_PRODUCTS_CHART = ROOT / "dataset_top_products.png"


def format_idr(value: float) -> str:
    return f"Rp{value:,.0f}".replace(",", ".")


def save_bar_chart(series: pd.Series, title: str, xlabel: str, ylabel: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=series.index, y=series.values, ax=ax, color="#2f6fed")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def save_horizontal_bar_chart(series: pd.Series, title: str, xlabel: str, ylabel: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(x=series.values, y=series.index, ax=ax, color="#2f6fed")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def save_line_chart(series: pd.Series, title: str, xlabel: str, ylabel: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=series.index, y=series.values, ax=ax, marker="o", linewidth=2.0, color="#d14b28")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def build_report(df: pd.DataFrame) -> str:
    invoice_summary = (
        df.groupby("nomor_struk")
        .agg(
            transaction_date=("tgl_transaksi", "first"),
            line_count=("kode_produk", "size"),
            unique_products=("kode_produk", "nunique"),
            units=("jumlah_terjual", "sum"),
            revenue=("total_nilai", "sum"),
        )
        .sort_values(["transaction_date", "revenue"], ascending=[True, False])
    )

    daily_summary = (
        df.groupby("tgl_transaksi")
        .agg(
            daily_revenue=("total_nilai", "sum"),
            daily_units=("jumlah_terjual", "sum"),
            daily_line_items=("kode_produk", "size"),
            daily_invoices=("nomor_struk", "nunique"),
        )
        .reset_index()
        .sort_values("tgl_transaksi")
    )
    daily_summary["avg_order_value"] = daily_summary["daily_revenue"] / daily_summary["daily_invoices"]

    product_summary = (
        df.groupby(["kode_produk", "nama_produk"])
        .agg(
            line_items=("nomor_struk", "size"),
            invoices=("nomor_struk", "nunique"),
            units=("jumlah_terjual", "sum"),
            revenue=("total_nilai", "sum"),
            avg_price=("harga", "mean"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    product_summary["revenue_share"] = product_summary["revenue"] / product_summary["revenue"].sum()
    product_summary["cumulative_revenue_share"] = product_summary["revenue_share"].cumsum()
    product_summary["abc_class"] = product_summary["cumulative_revenue_share"].map(
        lambda value: "A" if value <= 0.80 else ("B" if value <= 0.95 else "C")
    )

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    weekday_summary = (
        df.groupby("weekday")
        .agg(
            daily_revenue=("total_nilai", "sum"),
            invoices=("nomor_struk", "nunique"),
            units=("jumlah_terjual", "sum"),
        )
        .reindex(weekday_order)
        .dropna()
    )
    weekday_summary["avg_order_value"] = weekday_summary["daily_revenue"] / weekday_summary["invoices"]

    monthly_summary = (
        df.assign(month=df["tgl_transaksi"].dt.to_period("M").astype(str))
        .groupby("month")
        .agg(
            revenue=("total_nilai", "sum"),
            invoices=("nomor_struk", "nunique"),
            line_items=("kode_produk", "size"),
        )
    )

    invoice_revenue_stats = invoice_summary["revenue"].describe(percentiles=[0.5, 0.75, 0.9, 0.95, 0.99])
    invoice_line_stats = invoice_summary["line_count"].describe(percentiles=[0.5, 0.75, 0.9, 0.95, 0.99])
    invoice_unit_stats = invoice_summary["units"].describe(percentiles=[0.5, 0.75, 0.9, 0.95, 0.99])

    product_price_points = (
        df.groupby(["kode_produk", "nama_produk"])["harga"]
        .nunique()
        .reset_index(name="price_points")
        .sort_values(["price_points", "kode_produk"], ascending=[False, True])
    )

    total_revenue = float(df["total_nilai"].sum())
    total_units = int(df["jumlah_terjual"].sum())
    total_invoices = int(df["nomor_struk"].nunique())
    total_line_items = int(len(df))
    product_count = int(df["kode_produk"].nunique())
    avg_order_value = total_revenue / total_invoices
    avg_units_per_invoice = total_units / total_invoices
    avg_lines_per_invoice = total_line_items / total_invoices
    price_consistency_rate = float((df["jumlah_terjual"] * df["harga"] == df["total_nilai"]).mean())
    duplicate_line_rate = float(df.duplicated().mean())
    variable_price_products = int((product_price_points["price_points"] > 1).sum())

    best_day = daily_summary.loc[daily_summary["daily_revenue"].idxmax()]
    weakest_day = daily_summary.loc[daily_summary["daily_revenue"].idxmin()]

    top_10_share = product_summary.head(10)["revenue"].sum() / total_revenue
    top_product = product_summary.iloc[0]
    low_velocity = product_summary.nsmallest(10, "units")
    class_counts = product_summary["abc_class"].value_counts().to_dict()

    lines = [
        "# Dataset Deep Dive",
        "",
        "Last updated: 2026-05-09",
        "",
        "## Scope",
        "",
        "This is a working analysis of the preview retail transaction dataset released before the hackathon task. It focuses on data quality, transaction shape, commercial patterns, and preparation angles that are useful before the actual question arrives.",
        "",
        "## Source",
        "",
        "- Dataset file: [dataset/Transaksi.csv](dataset/Transaksi.csv)",
        "- Analysis script: [analyze_transaksi_dataset.py](analyze_transaksi_dataset.py)",
        "",
        "## Dataset Snapshot",
        "",
        f"- Rows: {total_line_items:,}",
        f"- Distinct invoices: {total_invoices:,}",
        f"- Distinct products: {product_count:,}",
        f"- Date coverage: {df['tgl_transaksi'].min().strftime('%Y-%m-%d')} to {df['tgl_transaksi'].max().strftime('%Y-%m-%d')}",
        f"- Distinct transaction days: {df['tgl_transaksi'].nunique():,}",
        f"- Total units sold: {total_units:,}",
        f"- Total gross sales value: {format_idr(total_revenue)}",
        f"- Average order value: {format_idr(avg_order_value)}",
        f"- Average units per invoice: {avg_units_per_invoice:.2f}",
        f"- Average line items per invoice: {avg_lines_per_invoice:.2f}",
        "",
        "## Schema",
        "",
        "- `nomor_struk`: invoice identifier",
        "- `tgl_transaksi`: transaction date",
        "- `kode_produk`: product code",
        "- `nama_produk`: product name",
        "- `jumlah_terjual`: quantity sold on the line item",
        "- `harga`: line-item unit price",
        "- `total_nilai`: line-item gross value",
        "",
        "## Data Quality Checks",
        "",
        "- Missing values: none detected across all 7 columns.",
        f"- Exact duplicate rows: {duplicate_line_rate:.2%} of rows.",
        f"- `jumlah_terjual * harga == total_nilai`: {price_consistency_rate:.2%} of rows.",
        f"- Products with more than one observed unit price: {variable_price_products:,}.",
        f"- Invoice grain check: {total_line_items - total_invoices:,} more line items than invoices, which is consistent with basket-style transaction data.",
        "",
        "## Core Business Patterns",
        "",
        f"- Best revenue day: {best_day['tgl_transaksi'].strftime('%Y-%m-%d')} with {format_idr(best_day['daily_revenue'])} across {int(best_day['daily_invoices']):,} invoices.",
        f"- Weakest revenue day: {weakest_day['tgl_transaksi'].strftime('%Y-%m-%d')} with {format_idr(weakest_day['daily_revenue'])} across {int(weakest_day['daily_invoices']):,} invoices.",
        f"- Top product by revenue: {top_product['nama_produk']} ({top_product['kode_produk']}) with {format_idr(top_product['revenue'])} and {int(top_product['units']):,} units sold.",
        f"- Revenue concentration: top 10 products contribute {top_10_share:.2%} of total revenue.",
        f"- ABC concentration: class A={class_counts.get('A', 0)}, class B={class_counts.get('B', 0)}, class C={class_counts.get('C', 0)} products.",
        f"- Basket-size signal: the maximum observed line items per invoice is {int(invoice_summary['line_count'].max())}, which suggests either a real operational pattern or an upstream generation cap.",
        "",
        "## Daily Trend Notes",
        "",
        f"- Mean daily revenue: {format_idr(daily_summary['daily_revenue'].mean())}",
        f"- Median daily revenue: {format_idr(daily_summary['daily_revenue'].median())}",
        f"- Mean daily invoice count: {daily_summary['daily_invoices'].mean():.2f}",
        f"- Mean daily units sold: {daily_summary['daily_units'].mean():.2f}",
        "",
        "## Month Coverage Notes",
        "",
    ]

    for month, row in monthly_summary.iterrows():
        lines.append(
            f"- {month}: revenue {format_idr(row['revenue'])}, invoices {int(row['invoices']):,}, line items {int(row['line_items']):,}"
        )

    lines.extend(
        [
            "",
            "## Invoice Distribution Notes",
            "",
            f"- Invoice revenue median: {format_idr(invoice_revenue_stats['50%'])}",
            f"- Invoice revenue 90th percentile: {format_idr(invoice_revenue_stats['90%'])}",
            f"- Invoice revenue 99th percentile: {format_idr(invoice_revenue_stats['99%'])}",
            f"- Maximum invoice revenue: {format_idr(invoice_revenue_stats['max'])}",
            f"- Median line items per invoice: {invoice_line_stats['50%']:.0f}",
            f"- 90th percentile line items per invoice: {invoice_line_stats['90%']:.0f}",
            f"- Maximum line items per invoice: {invoice_line_stats['max']:.0f}",
            f"- Median units per invoice: {invoice_unit_stats['50%']:.0f}",
            f"- 90th percentile units per invoice: {invoice_unit_stats['90%']:.0f}",
            f"- Maximum units per invoice: {invoice_unit_stats['max']:.0f}",
            "",
            "## Pricing Notes",
            "",
            f"- All {product_count:,} products have a single observed unit price across the dataset.",
            "- No discount field or explicit promo signal is present in the raw data.",
            "- This makes ranking and contribution analysis straightforward, but weakens any true price-elasticity analysis before the task adds more context.",
            "",
            "## Weekday Pattern Notes",
            "",
        ]
    )

    for weekday, row in weekday_summary.iterrows():
        lines.append(
            f"- {weekday}: revenue {format_idr(row['daily_revenue'])}, invoices {int(row['invoices']):,}, AOV {format_idr(row['avg_order_value'])}"
        )

    lines.extend(
        [
            "",
            "## Top 10 Products by Revenue",
            "",
            "| Rank | Product | Code | Revenue | Units | Invoices | Revenue Share |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )

    for rank, row in product_summary.head(10).reset_index(drop=True).iterrows():
        lines.append(
            "| {rank} | {product} | {code} | {revenue} | {units:,} | {invoices:,} | {share:.2%} |".format(
                rank=rank + 1,
                product=row["nama_produk"],
                code=row["kode_produk"],
                revenue=format_idr(row["revenue"]),
                units=int(row["units"]),
                invoices=int(row["invoices"]),
                share=row["revenue_share"],
            )
        )

    lines.extend(
        [
            "",
            "## Low Velocity Products by Units Sold",
            "",
            "| Product | Code | Units | Revenue | Invoices |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )

    for _, row in low_velocity.iterrows():
        lines.append(
            "| {product} | {code} | {units:,} | {revenue} | {invoices:,} |".format(
                product=row["nama_produk"],
                code=row["kode_produk"],
                units=int(row["units"]),
                revenue=format_idr(row["revenue"]),
                invoices=int(row["invoices"]),
            )
        )

    lines.extend(
        [
            "",
            "## Top 10 Invoices by Revenue",
            "",
            "| Invoice | Date | Revenue | Units | Line Items | Distinct Products |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )

    for invoice_id, row in invoice_summary.sort_values("revenue", ascending=False).head(10).iterrows():
        lines.append(
            "| {invoice_id} | {date} | {revenue} | {units:,} | {line_count:,} | {unique_products:,} |".format(
                invoice_id=invoice_id,
                date=row["transaction_date"].strftime("%Y-%m-%d"),
                revenue=format_idr(row["revenue"]),
                units=int(row["units"]),
                line_count=int(row["line_count"]),
                unique_products=int(row["unique_products"]),
            )
        )

    lines.extend(
        [
            "",
            "## Prep Recommendations Before the Task Arrives",
            "",
            "- Assume the task will be built on line-item transaction analysis, so keep invoice-level and product-level aggregation helpers ready.",
            "- Expect questions around revenue ranking, sales trends, product contribution, or basket-level metrics because the dataset is already clean and transaction-shaped.",
            "- Be ready to explain the date range carefully: the preview data is not only February; it spills into early March.",
            "- Be ready to mention price stability: every product currently appears at a single fixed price in the dataset.",
            "- Keep date parsing explicit using day-first format because the raw CSV uses `dd-mm-yyyy`.",
            "- Preserve a validation step for `jumlah_terjual * harga == total_nilai`; it is currently perfectly consistent and may be expected in downstream answers.",
            "- If the task introduces visualization, the daily sales trend and top-product ranking are already strong default views.",
            "",
            "## Confidence",
            "",
            "- High confidence: dataset shape, date coverage, data quality checks, revenue totals, invoice counts, product counts, price stability, and top-product ranking. These are direct calculations from the CSV.",
            "- Medium confidence: likely task directions such as trend analysis, leaderboard-style ranking, basket analysis, and product contribution questions. These are informed guesses based on the dataset shape, not official instructions.",
            "- Low confidence: any category-based business interpretation beyond what is directly in product names, because no product hierarchy, margin field, customer field, or store field is provided.",
            "",
            "## Generated Artifacts",
            "",
            "- [dataset_daily_revenue.png](dataset_daily_revenue.png)",
            "- [dataset_weekday_revenue.png](dataset_weekday_revenue.png)",
            "- [dataset_top_products.png](dataset_top_products.png)",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    sns.set_theme(style="whitegrid")

    df = pd.read_csv(DATASET_PATH)
    df["tgl_transaksi"] = pd.to_datetime(df["tgl_transaksi"], format="%d-%m-%Y")
    df["weekday"] = df["tgl_transaksi"].dt.day_name()

    daily_revenue = df.groupby("tgl_transaksi")["total_nilai"].sum().sort_index()
    weekday_revenue = (
        df.groupby("weekday")["total_nilai"]
        .sum()
        .reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        .dropna()
    )
    top_products = (
        df.groupby("nama_produk")["total_nilai"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values(ascending=True)
    )

    save_line_chart(
        daily_revenue,
        title="Daily Revenue Trend",
        xlabel="Transaction Date",
        ylabel="Revenue",
        path=DAILY_REVENUE_CHART,
    )
    save_bar_chart(
        weekday_revenue,
        title="Revenue by Weekday",
        xlabel="Weekday",
        ylabel="Revenue",
        path=WEEKDAY_REVENUE_CHART,
    )
    save_horizontal_bar_chart(
        top_products,
        title="Top 10 Products by Revenue",
        xlabel="Revenue",
        ylabel="Product",
        path=TOP_PRODUCTS_CHART,
    )

    REPORT_PATH.write_text(build_report(df), encoding="utf-8")
    print(f"Wrote report to {REPORT_PATH}")
    print(f"Saved charts to {DAILY_REVENUE_CHART.name}, {WEEKDAY_REVENUE_CHART.name}, {TOP_PRODUCTS_CHART.name}")


if __name__ == "__main__":
    main()