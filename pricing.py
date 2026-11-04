"""价格计算模块。

单位统一为「分」(int)，避免浮点货币误差。
预期舍入规则见 README：折扣额按四舍五入取整。
"""


def apply_discount(price_cents: int, discount_pct: int) -> int:
    """返回打折后的应付金额（分）。

    折扣额应先按四舍五入取整，再从原价中扣除。
    """
    discount = int(price_cents * discount_pct / 100)
    return price_cents - discount


def shipping_fee(weight_grams: int) -> int:
    """阶梯运费（分）：首 1000g 收 800，之后每满 500g 加收 300，不足一档按一档计。

    非正重量返回 0。
    """
    if weight_grams <= 0:
        return 0
    fee = 800
    if weight_grams > 1000:
        extra_units = -(-(weight_grams - 1000) // 500)
        fee += extra_units * 300
    return fee
