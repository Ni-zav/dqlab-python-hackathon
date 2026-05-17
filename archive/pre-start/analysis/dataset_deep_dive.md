# Dataset Deep Dive

Last updated: 2026-05-09

## Scope

This is a working analysis of the preview retail transaction dataset released before the hackathon task. It focuses on data quality, transaction shape, commercial patterns, and preparation angles that are useful before the actual question arrives.

## Source

- Dataset file: [dataset/Transaksi.csv](dataset/Transaksi.csv)
- Analysis script: [analyze_transaksi_dataset.py](analyze_transaksi_dataset.py)

## Dataset Snapshot

- Rows: 42,446
- Distinct invoices: 9,403
- Distinct products: 58
- Date coverage: 2025-02-01 to 2025-03-04
- Distinct transaction days: 32
- Total units sold: 97,078
- Total gross sales value: Rp3.439.447.500
- Average order value: Rp365.782
- Average units per invoice: 10.32
- Average line items per invoice: 4.51

## Schema

- `nomor_struk`: invoice identifier
- `tgl_transaksi`: transaction date
- `kode_produk`: product code
- `nama_produk`: product name
- `jumlah_terjual`: quantity sold on the line item
- `harga`: line-item unit price
- `total_nilai`: line-item gross value

## Data Quality Checks

- Missing values: none detected across all 7 columns.
- Exact duplicate rows: 0.00% of rows.
- `jumlah_terjual * harga == total_nilai`: 100.00% of rows.
- Products with more than one observed unit price: 0.
- Invoice grain check: 33,043 more line items than invoices, which is consistent with basket-style transaction data.

## Core Business Patterns

- Best revenue day: 2025-02-05 with Rp123.825.000 across 337 invoices.
- Weakest revenue day: 2025-03-03 with Rp70.382.000 across 158 invoices.
- Top product by revenue: Kaos Kaki (3 Pasang) (KSKK3P) with Rp310.125.000 and 12,405 units sold.
- Revenue concentration: top 10 products contribute 41.67% of total revenue.
- ABC concentration: class A=34, class B=14, class C=10 products.
- Basket-size signal: the maximum observed line items per invoice is 10, which suggests either a real operational pattern or an upstream generation cap.

## Daily Trend Notes

- Mean daily revenue: Rp107.482.734
- Median daily revenue: Rp109.616.250
- Mean daily invoice count: 293.84
- Mean daily units sold: 3033.69

## Month Coverage Notes

- 2025-02: revenue Rp3.081.546.500, invoices 8,471, line items 37,918
- 2025-03: revenue Rp357.901.000, invoices 932, line items 4,528

## Invoice Distribution Notes

- Invoice revenue median: Rp290.000
- Invoice revenue 90th percentile: Rp835.400
- Invoice revenue 99th percentile: Rp1.260.900
- Maximum invoice revenue: Rp2.055.000
- Median line items per invoice: 4
- 90th percentile line items per invoice: 9
- Maximum line items per invoice: 10
- Median units per invoice: 9
- 90th percentile units per invoice: 22
- Maximum units per invoice: 43

## Pricing Notes

- All 58 products have a single observed unit price across the dataset.
- No discount field or explicit promo signal is present in the raw data.
- This makes ranking and contribution analysis straightforward, but weakens any true price-elasticity analysis before the task adds more context.

## Weekday Pattern Notes

- Monday: revenue Rp523.108.500, invoices 1,452, AOV Rp360.268
- Tuesday: revenue Rp504.555.000, invoices 1,362, AOV Rp370.452
- Wednesday: revenue Rp445.736.500, invoices 1,230, AOV Rp362.387
- Thursday: revenue Rp453.805.500, invoices 1,227, AOV Rp369.850
- Friday: revenue Rp421.838.500, invoices 1,160, AOV Rp363.654
- Saturday: revenue Rp560.166.500, invoices 1,449, AOV Rp386.588
- Sunday: revenue Rp530.237.000, invoices 1,523, AOV Rp348.153

## Top 10 Products by Revenue

| Rank | Product | Code | Revenue | Units | Invoices | Revenue Share |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| 1 | Kaos Kaki (3 Pasang) | KSKK3P | Rp310.125.000 | 12,405 | 7,180 | 9.02% |
| 2 | Teko Listrik | TEKOLT | Rp242.525.000 | 2,725 | 1,533 | 7.05% |
| 3 | Kabel Data Fast Charge | KBLCHG | Rp235.292.000 | 3,988 | 1,139 | 6.84% |
| 4 | Mouse Wireless | MSWRLS | Rp199.125.000 | 2,655 | 1,201 | 5.79% |
| 5 | Sabun Cuci Cair 1.5L | SCC15L | Rp95.970.000 | 2,742 | 905 | 2.79% |
| 6 | Cairan Pembersih Lantai 2L | CPL2L | Rp73.755.000 | 2,682 | 665 | 2.14% |
| 7 | Lampu LED Rumah 15W | LED15W | Rp73.395.000 | 1,165 | 378 | 2.13% |
| 8 | Deterjen Bubuk 800g | DTG800 | Rp72.162.000 | 2,532 | 1,666 | 2.10% |
| 9 | Garam Dapur (3 Pack) | GRMDAP | Rp65.520.000 | 6,240 | 1,535 | 1.90% |
| 10 | Speaker Bluetooth Portabel | SPKBT | Rp65.404.000 | 664 | 220 | 1.90% |

## Low Velocity Products by Units Sold

| Product | Code | Units | Revenue | Invoices |
| --- | --- | ---: | ---: | ---: |
| Tas Belanja Reusable | TASBLJ | 226 | Rp17.402.000 | 89 |
| Kaos Polos Katun | KOSPLN | 241 | Rp12.893.500 | 159 |
| Set Alat Makan Stainless | ALMAKS | 258 | Rp16.641.000 | 59 |
| Jas Hujan Plastik | JASHJN | 272 | Rp19.176.000 | 92 |
| Botol Minum Plastik | BTLPLT | 387 | Rp18.189.000 | 129 |
| Bantal Tidur Silikon | BANTAL | 412 | Rp27.398.000 | 164 |
| Powerbank 5000mAh | PWBNK5 | 421 | Rp41.047.500 | 139 |
| Susu Formula Anak (Box) | SUFORA | 435 | Rp24.795.000 | 290 |
| Setrika Listrik Standar | STRIKA | 483 | Rp48.058.500 | 237 |
| Wajan Enamel Anti Lengket | WJANEM | 553 | Rp44.240.000 | 161 |

## Top 10 Invoices by Revenue

| Invoice | Date | Revenue | Units | Line Items | Distinct Products |
| --- | --- | ---: | ---: | ---: | ---: |
| INV-00000324 | 2025-02-02 | Rp2.055.000 | 35 | 10 | 10 |
| INV-00006398 | 2025-02-22 | Rp1.817.000 | 38 | 10 | 10 |
| INV-00004753 | 2025-02-17 | Rp1.806.000 | 30 | 10 | 10 |
| INV-00009265 | 2025-03-04 | Rp1.803.000 | 25 | 9 | 9 |
| INV-00001096 | 2025-02-04 | Rp1.731.500 | 34 | 10 | 10 |
| INV-00002263 | 2025-02-08 | Rp1.718.000 | 33 | 10 | 10 |
| INV-00000158 | 2025-02-01 | Rp1.690.000 | 36 | 10 | 10 |
| INV-00003850 | 2025-02-14 | Rp1.685.000 | 26 | 9 | 9 |
| INV-00001884 | 2025-02-07 | Rp1.663.500 | 31 | 10 | 10 |
| INV-00005367 | 2025-02-19 | Rp1.648.000 | 30 | 9 | 9 |

## Prep Recommendations Before the Task Arrives

- Assume the task will be built on line-item transaction analysis, so keep invoice-level and product-level aggregation helpers ready.
- Expect questions around revenue ranking, sales trends, product contribution, or basket-level metrics because the dataset is already clean and transaction-shaped.
- Be ready to explain the date range carefully: the preview data is not only February; it spills into early March.
- Be ready to mention price stability: every product currently appears at a single fixed price in the dataset.
- Keep date parsing explicit using day-first format because the raw CSV uses `dd-mm-yyyy`.
- Preserve a validation step for `jumlah_terjual * harga == total_nilai`; it is currently perfectly consistent and may be expected in downstream answers.
- If the task introduces visualization, the daily sales trend and top-product ranking are already strong default views.

## Confidence

- High confidence: dataset shape, date coverage, data quality checks, revenue totals, invoice counts, product counts, price stability, and top-product ranking. These are direct calculations from the CSV.
- Medium confidence: likely task directions such as trend analysis, leaderboard-style ranking, basket analysis, and product contribution questions. These are informed guesses based on the dataset shape, not official instructions.
- Low confidence: any category-based business interpretation beyond what is directly in product names, because no product hierarchy, margin field, customer field, or store field is provided.

## Generated Artifacts

- [dataset_daily_revenue.png](dataset_daily_revenue.png)
- [dataset_weekday_revenue.png](dataset_weekday_revenue.png)
- [dataset_top_products.png](dataset_top_products.png)
