from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT.parent / "dataset" / "Transaksi.csv"
OUTPUT_DIR = ROOT / "submission_prep"


@dataclass(frozen=True)
class DatasetProfile:
    rows: int
    invoices: int
    products: int
    date_min: str
    date_max: str
    total_units: int
    total_revenue: int


def format_idr(value: float) -> str:
    return f"Rp{value:,.0f}".replace(",", ".")


def load_transactions(path: Path = DATASET_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["tgl_transaksi"] = pd.to_datetime(df["tgl_transaksi"], format="%d-%m-%Y")
    df["weekday"] = df["tgl_transaksi"].dt.day_name()
    df["month"] = df["tgl_transaksi"].dt.to_period("M").astype(str)
    return df


def build_profile(df: pd.DataFrame) -> DatasetProfile:
    return DatasetProfile(
        rows=int(len(df)),
        invoices=int(df["nomor_struk"].nunique()),
        products=int(df["kode_produk"].nunique()),
        date_min=df["tgl_transaksi"].min().strftime("%Y-%m-%d"),
        date_max=df["tgl_transaksi"].max().strftime("%Y-%m-%d"),
        total_units=int(df["jumlah_terjual"].sum()),
        total_revenue=int(df["total_nilai"].sum()),
    )


def validate_transactions(df: pd.DataFrame) -> dict[str, float]:
    return {
        "missing_rate": float(df.isna().any(axis=1).mean()),
        "duplicate_rate": float(df.duplicated().mean()),
        "price_consistency_rate": float((df["jumlah_terjual"] * df["harga"] == df["total_nilai"]).mean()),
        "variable_price_products": float(
            df.groupby(["kode_produk", "nama_produk"])["harga"].nunique().gt(1).sum()
        ),
    }


def invoice_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
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


def daily_summary(df: pd.DataFrame) -> pd.DataFrame:
    daily = (
        df.groupby("tgl_transaksi")
        .agg(
            revenue=("total_nilai", "sum"),
            invoices=("nomor_struk", "nunique"),
            units=("jumlah_terjual", "sum"),
            line_items=("kode_produk", "size"),
        )
        .sort_index()
    )
    daily["avg_order_value"] = daily["revenue"] / daily["invoices"]
    return daily


def weekday_summary(df: pd.DataFrame) -> pd.DataFrame:
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday = (
        df.groupby("weekday")
        .agg(revenue=("total_nilai", "sum"), invoices=("nomor_struk", "nunique"), units=("jumlah_terjual", "sum"))
        .reindex(order)
        .dropna()
    )
    weekday["avg_order_value"] = weekday["revenue"] / weekday["invoices"]
    return weekday


def product_summary(df: pd.DataFrame) -> pd.DataFrame:
    products = (
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
    products["revenue_share"] = products["revenue"] / products["revenue"].sum()
    products["cumulative_revenue_share"] = products["revenue_share"].cumsum()
    products["abc_class"] = products["cumulative_revenue_share"].map(
        lambda value: "A" if value <= 0.80 else ("B" if value <= 0.95 else "C")
    )
    return products


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("month")
        .agg(revenue=("total_nilai", "sum"), invoices=("nomor_struk", "nunique"), line_items=("kode_produk", "size"))
        .sort_index()
    )


def top_invoices(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return invoice_summary(df).sort_values("revenue", ascending=False).head(n)


def write_markdown_summary(df: pd.DataFrame, output_path: Path) -> None:
    profile = build_profile(df)
    checks = validate_transactions(df)
    daily = daily_summary(df)
    products = product_summary(df)
    invoices = top_invoices(df)

    lines = [
        "# Submission Prep Summary",
        "",
        "This file is the reusable starting point for the final task solution. Replace the placeholders with the actual question logic when it arrives.",
        "",
        "## Snapshot",
        "",
        f"- Rows: {profile.rows:,}",
        f"- Distinct invoices: {profile.invoices:,}",
        f"- Distinct products: {profile.products:,}",
        f"- Date range: {profile.date_min} to {profile.date_max}",
        f"- Total units: {profile.total_units:,}",
        f"- Total revenue: {format_idr(profile.total_revenue)}",
        "",
        "## Validation",
        "",
        f"- Missing rate: {checks['missing_rate']:.2%}",
        f"- Duplicate row rate: {checks['duplicate_rate']:.2%}",
        f"- Price consistency rate: {checks['price_consistency_rate']:.2%}",
        f"- Variable price products: {int(checks['variable_price_products']):,}",
        "",
        "## Suggested Task Angles",
        "",
        "- Revenue ranking",
        "- Daily or weekday trend",
        "- Product contribution and ABC analysis",
        "- Basket analysis at invoice level",
        "- Top invoice outlier inspection",
        "",
        "## Ready-Made Objects",
        "",
        f"- Daily rows: {len(daily):,}",
        f"- Product rows: {len(products):,}",
        f"- Top invoices rows: {len(invoices):,}",
        "",
        "## Next Step Placeholder",
        "",
        "Fill the section below once the real task arrives:",
        "",
        "```text",
        "TASK QUESTION:",
        "APPROACH:",
        "OUTPUT:",
        "VALIDATION:",
        "```",
        "",
    ]

    output_path.write_text("\n".join(lines), encoding="utf-8")


def plot_daily_revenue(df: pd.DataFrame, output_dir: Path) -> Path:
    daily = daily_summary(df)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=daily.index, y=daily["revenue"], marker="o", ax=ax, color="#d14b28")
    ax.set_title("Daily Revenue Trend")
    ax.set_xlabel("Transaction Date")
    ax.set_ylabel("Revenue")
    fig.tight_layout()
    path = output_dir / "daily_revenue_template.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_top_products(df: pd.DataFrame, output_dir: Path, top_n: int = 10) -> Path:
    products = product_summary(df).head(top_n).sort_values("revenue", ascending=True)
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(x=products["revenue"], y=products["nama_produk"], ax=ax, color="#2f6fed")
    ax.set_title(f"Top {top_n} Products by Revenue")
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Product")
    fig.tight_layout()
    path = output_dir / "top_products_template.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = load_transactions()

    write_markdown_summary(df, ROOT / "submission_prep_summary.md")
    plot_daily_revenue(df, OUTPUT_DIR)
    plot_top_products(df, OUTPUT_DIR)

    print("Prepared reusable submission template artifacts.")


if __name__ == "__main__":
    main()
