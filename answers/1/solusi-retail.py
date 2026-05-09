from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = Path.cwd()


@dataclass(frozen=True)
class RisingSession:
    kode_produk: str
    nama_produk: str
    growth_pct: float
    total_penjualan: int


def resolve_input_workbook() -> Path:
    candidates = [
        OUTPUT_DIR / "data_penjualan.xlsx",
        SCRIPT_DIR / "data_penjualan.xlsx",
        SCRIPT_DIR.parent.parent / "tasks" / "data_penjualan.xlsx",
        OUTPUT_DIR / "tasks" / "data_penjualan.xlsx",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError("data_penjualan.xlsx not found in working directory or fallback task paths")


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path)
    df["tgl_transaksi"] = pd.to_datetime(df["tgl_transaksi"])
    return df


def build_daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    daily = (
        df.groupby(["kode_produk", "nama_produk", "tgl_transaksi"], as_index=False)["total_nilai"]
        .sum()
        .sort_values(["kode_produk", "tgl_transaksi"])
    )
    return daily


def compute_rising_star_sessions(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    daily = build_daily_sales(df)
    total_sales = (
        df.groupby(["kode_produk", "nama_produk"], as_index=False)["total_nilai"]
        .sum()
        .rename(columns={"total_nilai": "Total Penjualan"})
    )

    report_rows: list[RisingSession] = []
    plot_frames: list[pd.DataFrame] = []

    for (kode_produk, nama_produk), group in daily.groupby(["kode_produk", "nama_produk"]):
        series = group.sort_values("tgl_transaksi").copy()
        series["MA"] = series["total_nilai"].rolling(window=3, min_periods=3).mean()
        series = series.dropna(subset=["MA"]).copy()
        if series.empty:
            continue

        series["is_rising"] = series["MA"].gt(series["MA"].shift(1))
        series["session_id"] = series["is_rising"].ne(series["is_rising"].shift()).cumsum()

        best_segment: pd.DataFrame | None = None
        best_growth: float | None = None

        for _, segment in series.groupby("session_id"):
            if not bool(segment["is_rising"].iloc[0]):
                continue
            if len(segment) < 12:
                continue

            start_value = float(segment["MA"].iloc[0])
            end_value = float(segment["MA"].iloc[-1])
            growth_pct = ((end_value - start_value) / start_value) * 100

            if best_segment is None or growth_pct > float(best_growth):
                best_segment = segment.copy()
                best_growth = growth_pct

        if best_segment is None or best_growth is None:
            continue

        total_penjualan = int(
            total_sales.loc[
                (total_sales["kode_produk"] == kode_produk) & (total_sales["nama_produk"] == nama_produk),
                "Total Penjualan",
            ].iloc[0]
        )

        best_segment["Normalized"] = (best_segment["MA"] / float(best_segment["MA"].iloc[0])) * 100
        best_segment["rank_source_growth"] = round(best_growth, 2)
        plot_frames.append(best_segment)

        report_rows.append(
            RisingSession(
                kode_produk=kode_produk,
                nama_produk=nama_produk,
                growth_pct=round(best_growth, 2),
                total_penjualan=total_penjualan,
            )
        )

    report = pd.DataFrame(
        [
            {
                "Kode Produk": row.kode_produk,
                "Nama Produk": row.nama_produk,
                "Growth %": row.growth_pct,
                "Total Penjualan": row.total_penjualan,
            }
            for row in report_rows
        ]
    )

    if report.empty:
        raise ValueError("No rising star products found from the source workbook")

    report = report.sort_values(["Growth %", "Total Penjualan"], ascending=[False, False]).reset_index(drop=True)

    plot_df = pd.concat(plot_frames, ignore_index=True)
    rank_map = {code: idx + 1 for idx, code in enumerate(report["Kode Produk"])}
    plot_df["rank"] = plot_df["kode_produk"].map(rank_map)
    plot_df = plot_df.sort_values(["rank", "tgl_transaksi"]).reset_index(drop=True)

    return report, plot_df


def build_top3_ma_plot_df(df: pd.DataFrame) -> pd.DataFrame:
    daily = build_daily_sales(df)
    top3_codes = (
        df.groupby(["kode_produk", "nama_produk"], as_index=False)["total_nilai"]
        .sum()
        .sort_values("total_nilai", ascending=False)
        .head(3)["kode_produk"]
        .tolist()
    )

    top3_df = daily[daily["kode_produk"].isin(top3_codes)].copy()
    top3_df["MA"] = (
        top3_df.groupby("kode_produk")["total_nilai"]
        .transform(lambda values: values.rolling(window=3, min_periods=3).mean())
    )
    top3_df = top3_df.dropna(subset=["MA"]).copy()
    top3_df["Normalized"] = top3_df.groupby("kode_produk")["MA"].transform(lambda values: (values / values.iloc[0]) * 100)
    return top3_df.sort_values(["kode_produk", "tgl_transaksi"]).reset_index(drop=True)


def build_top3_actual_plot_df(df: pd.DataFrame) -> pd.DataFrame:
    daily = build_daily_sales(df)
    top3_codes = (
        df.groupby(["kode_produk", "nama_produk"], as_index=False)["total_nilai"]
        .sum()
        .sort_values("total_nilai", ascending=False)
        .head(3)["kode_produk"]
        .tolist()
    )
    return daily[daily["kode_produk"].isin(top3_codes)].copy().sort_values(["kode_produk", "tgl_transaksi"])


def format_rule_items(items: frozenset[str], order_map: dict[str, int]) -> str:
    return ", ".join(sorted(items, key=lambda item: order_map.get(item, 10**9)))


def compute_potential_packaging(df: pd.DataFrame, rising_star_report: pd.DataFrame) -> pd.DataFrame:
    rising_names = set(rising_star_report["Nama Produk"])
    product_order = {name: idx for idx, name in enumerate(df["nama_produk"].drop_duplicates())}

    invoice_items = (
        df.drop_duplicates(["nomor_struk", "nama_produk"])
        .assign(present=True)
        .pivot(index="nomor_struk", columns="nama_produk", values="present")
        .fillna(False)
    )

    frequent_itemsets = apriori(invoice_items.astype(bool), min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
    rules = rules[rules["lift"] >= 2].copy()
    rules = rules[
        rules["antecedents"].apply(lambda values: any(item in rising_names for item in values))
        | rules["consequents"].apply(lambda values: any(item in rising_names for item in values))
    ].copy()

    rules["Jika Membeli"] = rules["antecedents"].apply(lambda values: format_rule_items(values, product_order))
    rules["Maka Membeli"] = rules["consequents"].apply(lambda values: format_rule_items(values, product_order))
    rules["Jumlah Invoice"] = (rules["support"] * len(invoice_items)).round().astype(int)

    output = rules[["Jika Membeli", "Maka Membeli", "Jumlah Invoice", "support", "confidence", "lift"]].copy()
    output = output.rename(columns={"support": "Support", "confidence": "Confidence", "lift": "Lift"})
    output = output.sort_values(["Lift", "Support", "Confidence", "Jika Membeli", "Maka Membeli"], ascending=[False, False, False, True, True]).reset_index(drop=True)
    output["Support"] = output["Support"].round(2)
    output["Confidence"] = output["Confidence"].round(2)
    output["Lift"] = output["Lift"].round(2)
    return output


def save_excel(rising_star_report: pd.DataFrame, potential_packaging: pd.DataFrame) -> None:
    output_path = OUTPUT_DIR / "retail_insight.xlsx"
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        rising_star_report.to_excel(writer, sheet_name="Rising Star", index=False)
        potential_packaging.to_excel(writer, sheet_name="Potential Packaging", index=False)


def build_color_maps(rising_star_report: pd.DataFrame) -> tuple[dict[str, str], dict[str, int]]:
    custom_palette = [
        "#FFD700",
        "#C0C0C0",
        "#CD7F32",
        "#2ecc71",
        "#3498db",
        "#9b59b6",
        "#e74c3c",
        "#34495e",
    ]
    default_color = "#95a5a6"

    color_mapping: dict[str, str] = {}
    rank_mapping: dict[str, int] = {}
    for index, row in enumerate(rising_star_report.itertuples(index=False), start=1):
        kode_produk = getattr(row, "_0")
        color_mapping[kode_produk] = custom_palette[index - 1] if index - 1 < len(custom_palette) else default_color
        rank_mapping[kode_produk] = index

    return color_mapping, rank_mapping


def sort_legend(ax: plt.Axes) -> None:
    handles, labels = ax.get_legend_handles_labels()
    top_sales_items: list[tuple[object, str]] = []
    rising_items: list[tuple[object, str]] = []

    for handle, label in zip(handles, labels):
        if label.startswith("Top Sales"):
            top_sales_items.append((handle, label))
        else:
            rising_items.append((handle, label))

    rising_items = sorted(rising_items, key=lambda item: int(item[1].split(":")[0].split()[1]))
    final_items = top_sales_items + rising_items

    ax.legend(
        [item[0] for item in final_items],
        [item[1] for item in final_items],
        title="Kategori Produk",
        title_fontsize=12,
        fontsize=10,
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        borderaxespad=0,
        frameon=True,
        shadow=True,
    )


def save_rising_star_index_chart(df: pd.DataFrame, rising_star_report: pd.DataFrame, plot_df: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(15, 8), dpi=100)
    ax = fig.add_subplot(111)

    color_mapping, rank_mapping = build_color_maps(rising_star_report)
    top3_plot_df = build_top3_ma_plot_df(df)
    grey_colors = ["#B0B0B0", "#909090", "#707070"]

    for idx, (kode_produk, group) in enumerate(top3_plot_df.groupby("kode_produk")):
        nama_produk = group["nama_produk"].iloc[0]
        grey_color = grey_colors[idx] if idx < len(grey_colors) else "#808080"
        ax.plot(
            group["tgl_transaksi"],
            group["Normalized"],
            linestyle="--",
            linewidth=2,
            marker="o",
            markersize=3,
            color=grey_color,
            alpha=0.7,
            label=f"Top Sales: {nama_produk}",
        )

    for kode_produk, group in plot_df.groupby("kode_produk"):
        nama_produk = group["nama_produk"].iloc[0]
        rank = rank_mapping[kode_produk]
        ax.plot(
            group["tgl_transaksi"],
            group["Normalized"],
            marker="o",
            markersize=4,
            linewidth=2.5,
            color=color_mapping[kode_produk],
            label=f"Rank {rank}: {nama_produk}",
        )

    ax.set_title(
        "ANALISIS PERTUMBUHAN RELATIF PRODUK RISING STAR\n(Dengan Benchmark Top 3 Total Penjualan)",
        fontdict={"family": "sans-serif", "color": "black", "weight": "bold", "size": 16},
        pad=20,
    )
    ax.set_xlabel("Periode Tanggal", fontdict={"family": "sans-serif", "weight": "normal", "size": 12}, labelpad=10)
    ax.set_ylabel("Indeks Pertumbuhan (Base 100)", fontdict={"family": "sans-serif", "weight": "normal", "size": 12}, labelpad=10)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
    ax.axhline(y=100, color="black", linestyle="-", linewidth=1, alpha=0.5)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(fontsize=10)
    sort_legend(ax)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "rising_star_index.png", bbox_inches="tight")
    plt.close(fig)


def save_rising_star_actual_chart(df: pd.DataFrame, rising_star_report: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(15, 8), dpi=100)
    ax = fig.add_subplot(111)

    color_mapping, rank_mapping = build_color_maps(rising_star_report)
    top3_actual_df = build_top3_actual_plot_df(df)
    top1_code = rising_star_report.iloc[0]["Kode Produk"]
    top1_name = rising_star_report.iloc[0]["Nama Produk"]

    grey_colors = ["#B0B0B0", "#909090", "#707070"]
    for idx, (kode_produk, group) in enumerate(top3_actual_df.groupby("kode_produk")):
        nama_produk = group["nama_produk"].iloc[0]
        grey_color = grey_colors[idx] if idx < len(grey_colors) else "#808080"
        ax.plot(
            group["tgl_transaksi"],
            group["total_nilai"],
            linestyle="--",
            linewidth=2,
            marker="o",
            markersize=3,
            color=grey_color,
            alpha=0.7,
            label=f"Top Sales: {nama_produk}",
        )

    top1_df = build_daily_sales(df)
    top1_df = top1_df[top1_df["kode_produk"] == top1_code].copy()
    ax.plot(
        top1_df["tgl_transaksi"],
        top1_df["total_nilai"],
        marker="o",
        markersize=4,
        linewidth=2.5,
        color=color_mapping[top1_code],
        label=f"Rank {rank_mapping[top1_code]}: {top1_name}",
    )

    ax.set_title(
        "ANALISIS NILAI PENJUALAN PRODUK RISING STAR\n(Nilai Penjualan Asli)",
        fontdict={"family": "sans-serif", "color": "black", "weight": "bold", "size": 16},
        pad=20,
    )
    ax.set_xlabel("Periode Tanggal", fontdict={"family": "sans-serif", "weight": "normal", "size": 12}, labelpad=10)
    ax.set_ylabel("Total Nilai Penjualan", fontdict={"family": "sans-serif", "weight": "normal", "size": 12}, labelpad=10)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(fontsize=10)
    sort_legend(ax)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "rising_star_actual.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    input_path = resolve_input_workbook()
    df = load_data(input_path)
    rising_star_report, rising_plot_df = compute_rising_star_sessions(df)
    potential_packaging = compute_potential_packaging(df, rising_star_report)

    save_excel(rising_star_report, potential_packaging)
    save_rising_star_index_chart(df, rising_star_report, rising_plot_df)
    save_rising_star_actual_chart(df, rising_star_report)

    print(f"Input workbook: {input_path}")
    print(f"Generated: {OUTPUT_DIR / 'retail_insight.xlsx'}")
    print(f"Generated: {OUTPUT_DIR / 'rising_star_index.png'}")
    print(f"Generated: {OUTPUT_DIR / 'rising_star_actual.png'}")


if __name__ == "__main__":
    main()