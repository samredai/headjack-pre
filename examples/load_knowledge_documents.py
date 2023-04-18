import headjack

hj = headjack.client()

hj.send(
    name="repair_orders",
    type="node",
    description="This tracks repair orders to all the roads in the city",
)

with open("knowledge/ten-years-after.txt", "r") as file:
    hj.send(
        name="ten_years_after",
        type="knowledge",
        description="This is an article about how NYC is not ready for another hurricane 10 years after hurricane Sandy.",
        content=file.read(),
        url=(
            "https://nyc.streetsblog.org/2022/10/28/"
            "ten-years-after-despite-warnings-and-panels-"
            "and-reports-new-york-is-not-ready-for-a-sandy-sequel/"
        ),
        metadata={},
    )
