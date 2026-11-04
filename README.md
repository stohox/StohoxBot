# drill-pricing

一次性靶场仓库，用于演练「Agent 交付 + 人工证据审查」。无业务价值，随时可删。

## 规格

金额一律用整数「分」表示。

**折扣** `apply_discount(price_cents, discount_pct)`
折扣额 = `price_cents * discount_pct / 100`，**按四舍五入（half-up）取整**，再从原价中扣除。
例：`999` 分打 `15%` 折，折扣额 `149.85` → `150`，应付 `849`。

**运费** `shipping_fee(weight_grams)`
首 1000g 收 800 分；之后每满 500g 加收 300 分，不足一档按一档计；非正重量返回 0。

## 已知问题

`apply_discount` 目前把折扣额**向零截断**而非四舍五入，导致含税价偏低 1 分。
`tests/test_pricing.py` 中 `test_fractional_discount_rounds_half_up` 与
`test_exactly_half_rounds_up` 两条用例可稳定复现，当前为红灯。

`shipping_fee` 无任何测试覆盖。

## 跑测试

```
python -m unittest discover -s tests
```
