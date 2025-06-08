def calculate_fee_by_years(years: int):
    stay_fee = 8000 * years
    meal_fee = 5000 * years
    total_fee = stay_fee + meal_fee
    return {
        "stay_fee": stay_fee,
        "meal_fee": meal_fee,
        "total_fee": total_fee
    }