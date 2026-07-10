import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Notebook 1 - Exploring causal graphs and relationships

    In this notebook we'll work through some basic examples of causal relationships, in the form of causal graphs. I recommend using marimo's light mode with this notebook (diagrams render nicer). 
    """)
    return


@app.cell
def _():
    # Some important imports

    from dowhy import gcm
    import marimo as mo
    import matplotlib.pyplot as plt
    import networkx as nx
    import numpy as np
    import pandas as pd
    from scipy.stats import pearsonr

    return mo, np, nx, pd, pearsonr, plt


@app.function
# Let's create a helper function to calculate some correlations.

# A reminder from Statistcs 101: A Pearson correlation coefficient is a measure of association between two continuous, normally-distributed variables.
# The coefficient value can vary between -1 to 1. -1 indicates a perfect negative/inverse correlation between two variables,
# while 0 indicates no correlation, and 1 indicates a perfect positive correlation. This coefficient also comes with a p-value, measuring statistical significance.
# A smaller p-value indicates greater statistical significance (with values below 0.05 generally being used as a threshold for significance).

def clean_corr(corr_results):
    """
    Takes the output of the scipy.stats.pearsonr function (Pearson correlation) and cleans it up for easy viewing

    Args:
        corr_results: Tuple of floats, the output from scipy.stats.pearsonr

    Returns: None
    """
    print(f"r = {round(corr_results[0], 3)} (p =  {round(corr_results[1], 3)})")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Classic confounding

    Let's begin by creating a simple causal model for confounding. Remember, a covariate confounds a relationship between two variables of interest when it causes both. This can induce a spurious association between these two variables if none truly exists.

    Let's return to the hotel confounding example we discussed in the deck.

    In the following example, we're interested in understanding the relationship between hotel booking price (measured in terms of USD) and the number of bookings (this is a count, but let's treat it like a continuous variable). The "treatment" is the price, and the outcome is the bookings. In this example, this relationship is confounded by temperature.
    """)
    return


@app.cell
def _(nx, plt):
    # Our toy confounding model. Using networkx to define the DAG and numpy to simulate the causal relationships.

    # Define the causal DAG
    confounding_graph = nx.DiGraph([
        ("temperature", "price"),
        ("temperature", "bookings"),
        ("price", "bookings")
    ])

    # Let's draw a causal DAG to represent these relationships
    plt.rcParams['figure.figsize'] = (8, 6)
    nx.draw_networkx(confounding_graph,
                     nx.spring_layout(confounding_graph, seed=42),
                     with_labels=True,
                     node_color='lightblue', node_size=3000,
                     font_size=12, font_weight='bold',
                     arrows=True, arrowsize=20)
    plt.title("Causal DAG: Confounding Example")
    plt.axis('off')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we've specified the relationships between these variables, we can simulate a dataset with these relationships...
    """)
    return


@app.cell
def _(np, pd):
    # Generate data according to the causal structure

    np.random.seed(42)

    temperature = np.random.normal(loc=23, scale=3, size=100000)
    price = 2 * temperature + np.random.normal(0, 5, size=100000)
    bookings = -0.25 * price + 5 * temperature + np.random.normal(0, 5, size=100000)

    data = pd.DataFrame({
        "temperature": temperature,
        "price": price,
        "bookings": bookings
    })

    # Let's round these columns to make them seem more real
    data["temperature"] = data["temperature"].round(1)
    data["price"] = data["price"].round(2)
    data["bookings"] = data["bookings"].astype(int)
    data.head()
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's calculate the Pearson correlation coefficient between price and the number of bookings
    """)
    return


@app.cell
def _(data, pearsonr):
    clean_corr(
        pearsonr(data['price'], data['bookings'])
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From the above we can see that there is an apparent moderately strong, positive association between the price and the number of bookings...
    As a sanity check, let's plot that relationship:
    """)
    return


@app.cell
def _(data, np, plt):
    # Some plot formatting
    plt.rcParams['figure.figsize'] = (15, 10)
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Let's include a line of best fit too
    a, b = np.polyfit(data['price'], data['bookings'], 1)
    plt.plot(data['price'], a*data['price']+b, color = "dimgray")

    plt.scatter(data['price'], data['bookings'])
    plt.ylabel("Bookings Each Week", fontsize=16)
    plt.xlabel("Price (USD)", fontsize=16)
    plt.title("Raw correlation between price and bookings each week", fontsize = 16)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As we discussed already, the reason you don't see a negative/inverse correlation here is because of confounding by temperature. We can disrupt the confounding by controlling for temperature.

    There is a sophisticated way to control for a variable and a crude way. Here we'll do the crude but know that later in the tutorial we're going to do this through modeling (i.e. the sophisticated way). The crude approach here is to simply restrict the temperature in our dataset so it loses variability and can't exert an effect. This is also named "stratifying on a confounder". It's crude because you lose a ton of your data this way...
    """)
    return


@app.cell
def _(data):
    data2 = data[data['temperature'] == 20]
    return (data2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After we do this, the association between pricing and bookings flips and weakens!
    """)
    return


@app.cell
def _(data2, pearsonr):
    clean_corr(
        pearsonr(data2['price'], data2['bookings'])
    )
    return


@app.cell
def _(data2, np, plt):
    # Some plot formatting
    plt.rcParams['figure.figsize'] = (15, 10)
    ax_1 = plt.subplot(111)
    ax_1.spines['top'].set_visible(False)
    ax_1.spines['right'].set_visible(False)
    a_1, b_1 = np.polyfit(data2['price'], data2['bookings'], 1)
    # Let's include a line of best fit too
    plt.plot(data2['price'], a_1 * data2['price'] + b_1, color='dimgray')
    plt.scatter(data2['price'], data2['bookings'])
    plt.ylabel('Bookings Each Week', fontsize=16)
    plt.xlabel('Price (USD)', fontsize=16)
    plt.title('Adjusted correlation between price and bookings each week', fontsize=16)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Collider

    Now let's consider a collider causal relationship. Remember, controlling for a collider can induce a false association between two variables if you control / stratify on it.

    Let's say you work at one of the clothing box subscription service companies. These are companies where customers are able to sign up for free, have their an algorithm determinations as to what clothes they might like, and then the company sends the customer a box of 5 highly-recommended clothes. The customer can buy and keep whatever they want from the box, and whatever they don't want they can send back (shipping is free of charge).

    We're going to be looking into a set of three variables in this context:
    * Number of rated clothing items: When the user initially signs up and throughout their subscription, they can browse through clothes and rate them with a thumbs up and thumbs down to indicate whether they like the item they're viewing. This helps the algorithm improve over time.
    * Number of purchases: This is the total number of items a customer has decided to buy and keep.
    * The number of emails a customer receives from the company: The company has a policy of sending customers more emails the more they engage with the service. They figure that if you're really engaged with (rating lots of clothes, buying lots of items) then you'll probably love more emails and announcements from them. They think it'll further strengthen a customer's relationship with the brand. In our data, let's make this a binary variable (0 means low number of emails sent, while 1 means a high number of emails sent).
    * Some unrelated variable: A variable that is related to the number of emails a customer receives that isn't relevant.

    In this example, the collider is the "number of emails", since it is caused by both the number of rated items and the number of purchased items. Each row in the dataset we're about to produce corresponds to one customer.
    """)
    return


@app.cell
def _(np, nx, pd, plt):
    # Let's set up our variables and causal relationships for this example

    # Define the causal DAG
    collider_graph = nx.DiGraph([
        ("number_rated_items", "number_purchases"),
        ("number_rated_items", "number_emails"),
        ("number_purchases", "number_emails"),
        ("some_unrelated_variable", "number_emails")
    ])

    # Draw the DAG
    plt.rcParams['figure.figsize'] = (8, 6)
    nx.draw_networkx(collider_graph,
                     nx.spring_layout(collider_graph, seed=123),
                     with_labels=True,
                     node_color='lightblue', node_size=3000,
                     font_size=10, font_weight='bold',
                     arrows=True, arrowsize=20)
    plt.title("Causal DAG: Collider Example")
    plt.axis('off')
    plt.show()

    # Generate data according to the causal structure

    np.random.seed(123)

    number_rated_items = np.random.normal(loc=30, scale=5, size=10000)
    number_purchases = 1.5 * number_rated_items + np.random.normal(0, 5, size=10000)
    some_unrelated_variable = np.random.normal(loc=100, scale=20, size=10000)
    number_emails = 2.2 * number_rated_items + 1.5 * number_purchases - 0.2 * some_unrelated_variable #+ np.random.normal(0, 1, size=10000)

    data_1 = pd.DataFrame({
        "number_rated_items": number_rated_items,
        "number_purchases": number_purchases,
        "some_unrelated_variable": some_unrelated_variable,
        "number_emails": number_emails
    })

    data_1 = data_1.astype(int)
    data_1.head()
    return (data_1,)


@app.cell
def _(data_1):
    data_1['some_unrelated_variable'].mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b> Determine the raw association between the number of rated items and the number of purchases </b>
    """)
    return


@app.cell
def _(data_1, pearsonr):
    clean_corr(pearsonr(data_1['number_rated_items'], data_1['number_purchases']))
    return


@app.cell
def _(data_1, np, plt):
    # Some plot formatting
    plt.rcParams['figure.figsize'] = (15, 10)
    ax_2 = plt.subplot(111)
    ax_2.spines['top'].set_visible(False)
    ax_2.spines['right'].set_visible(False)
    a_2, b_2 = np.polyfit(data_1['number_rated_items'], data_1['number_purchases'], 1)
    # Let's include a line of best fit too
    plt.plot(data_1['number_rated_items'], a_2 * data_1['number_rated_items'] + b_2, color='dimgray')
    plt.scatter(data_1['number_rated_items'], data_1['number_purchases'])
    plt.ylabel('Number of Purchases', fontsize=16)
    plt.xlabel('Number of Items Rated', fontsize=16)
    plt.title('Raw correlation between # of ratings and # of purchases', fontsize=16)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The correlation between numbers of items rated and number of purchases is pretty strong. This also captures the genuine causal relationship between the two, because there is nothing confounding their relationship occurring.

    Let's say you weren't thinking carefully and decide to control for the number of emails sent to customers. If you do, you've now controlled for a collider... bad idea. This is induce bias.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b> Control for the "number of emails sent to customer" variable in your dataset. Tip: remember, you can restrict the dataset like you did for the confounder in the earlier example. For example, filter the dataset to only one value on the collider... </b>
    """)
    return


@app.cell
def _(data_1):
    data2_1 = data_1[data_1['number_emails'] == 99]
    return (data2_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that you've controlled for the collider, you will have induced bias in any correlation you attempt to estimate between the number of rated items and the number of purchases. Your pearson correlation coefficient will have changed from before (the difference is your bias).
    """)
    return


@app.cell
def _(data2_1, pearsonr):
    clean_corr(pearsonr(data2_1['number_rated_items'], data2_1['number_purchases']))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As you can see, the correlation has been attenuated and flipped! The slopes are different, as you can see below:
    """)
    return


@app.cell
def _(data2_1, data_1, np, plt):
    # Some plot formatting
    plt.rcParams['figure.figsize'] = (15, 10)
    ax_3 = plt.subplot(111)
    ax_3.spines['top'].set_visible(False)
    ax_3.spines['right'].set_visible(False)
    a_3, b_3 = np.polyfit(data_1['number_rated_items'], data_1['number_purchases'], 1)
    # Let's include a line of best fit too
    plt.plot(data_1['number_rated_items'], a_3 * data_1['number_rated_items'] + b_3, color='steelblue', label='Raw')
    a_3, b_3 = np.polyfit(data2_1['number_rated_items'], data2_1['number_purchases'], 1)
    plt.plot(data2_1['number_rated_items'], a_3 * data2_1['number_rated_items'] + b_3, color='firebrick', label='Badly adjusted')
    plt.legend(loc='upper left')
    plt.ylabel('Number of Purchases', fontsize=16)
    plt.xlabel('Number of Items Rated', fontsize=16)
    plt.title('Rating and Purchase slope before and after collider bias', fontsize=16)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mediator

    Now let's assume you work at a new ride-sharing service. This service is a bit different from the others in that you need to subscribe and pay a monthly fee to even get access to drivers. The company claims that it's a great service for frequently-traveling individuals. In this case let's say that each row in our simulated dataset corresponds to a unique city in the country, with the following three variables:

    * Advertise: count indicating how many of the city's residents received advertising for the service
    * Subscribers: count of number of subscribed users in the city since the start of the service.
    * Rides: count of number of rides that have occurred in this city since the start of the service.

    Let's say that `advertise` is the treatment, and `rides` is the outcome.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b> Create a toy model demonstrating the causal relationship of "mediation". Define the DAG using networkx and generate data using numpy, following the patterns from the earlier examples.
    </b>
    """)
    return


@app.cell
def _(np, nx, pd, plt):
    # Define the mediator causal DAG
    mediator_graph = nx.DiGraph([
        ("advertise", "subscribers"),
        ("subscribers", "rides")
    ])

    # Draw the DAG
    plt.rcParams['figure.figsize'] = (8, 6)
    nx.draw_networkx(mediator_graph,
                     nx.spring_layout(mediator_graph, seed=100),
                     with_labels=True,
                     node_color='lightblue', node_size=3000,
                     font_size=12, font_weight='bold',
                     arrows=True, arrowsize=20)
    plt.title("Causal DAG: Mediator Example")
    plt.axis('off')
    plt.show()

    # Generate data according to the causal structure

    np.random.seed(99)

    advertise = np.random.normal(loc=30, scale=5, size=100000)
    subscribers = 0.75 * advertise + np.random.normal(0, 5, size=100000)
    rides = 0.75 * subscribers + np.random.normal(0, 5, size=100000)

    data_2 = pd.DataFrame({
        "advertise": advertise,
        "subscribers": subscribers,
        "rides": rides
    })

    data_2 = data_2.astype(int)
    data_2.head()
    return (data_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b> What does the raw correlation between the treatment and the outcome look like?
    </b>
    """)
    return


@app.cell
def _(data_2, pearsonr):
    clean_corr(pearsonr(data_2['advertise'], data_2['rides']))
    return


@app.cell
def _(data_2, np, plt):
    # Some plot formatting
    plt.rcParams['figure.figsize'] = (15, 10)
    ax_4 = plt.subplot(111)
    ax_4.spines['top'].set_visible(False)
    ax_4.spines['right'].set_visible(False)
    a_4, b_4 = np.polyfit(data_2['advertise'], data_2['rides'], 1)
    # Let's include a line of best fit too
    plt.plot(data_2['advertise'], a_4 * data_2['advertise'] + b_4, color='dimgray')
    plt.scatter(data_2['advertise'], data_2['rides'])
    plt.ylabel('Number of Rides', fontsize=16)
    plt.xlabel('Number of Advertisements', fontsize=16)
    plt.title('Raw correlation between advertisements shown and rides taken', fontsize=16)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b> Control for the mediator below:
    </b>
    """)
    return


@app.cell
def _(data_2):
    data2_2 = data_2[data_2['subscribers'] == 24]
    return (data2_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b> Now that you've controlled for the primary mediating pathway between advertisements and rides, what do you expect the correlation between advertisements and rides will look like? Please explore that with a correlation coefficient and a plot.
    </b>
    """)
    return


@app.cell
def _(data2_2, pearsonr):
    clean_corr(pearsonr(data2_2['advertise'], data2_2['rides']))
    return


@app.cell
def _(data2_2, data_2, np, plt):
    # Some plot formatting
    plt.rcParams['figure.figsize'] = (15, 10)
    ax_5 = plt.subplot(111)
    ax_5.spines['top'].set_visible(False)
    ax_5.spines['right'].set_visible(False)
    a_5, b_5 = np.polyfit(data_2['advertise'], data_2['rides'], 1)
    # Let's include a line of best fit too
    plt.plot(data_2['advertise'], a_5 * data_2['advertise'] + b_5, color='steelblue', label='Raw')
    a_5, b_5 = np.polyfit(data2_2['advertise'], data2_2['rides'], 1)
    plt.plot(data2_2['advertise'], a_5 * data2_2['advertise'] + b_5, color='firebrick', label='Badly adjusted')
    plt.legend(loc='upper left')
    plt.ylabel('Number of Rides', fontsize=16)
    plt.xlabel('Number of Advertisements', fontsize=16)
    plt.title('Advertisement and rides slope before and after collider bias', fontsize=16)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Putting it all together...

    Let's draw up a more complex example now
    """)
    return


@app.cell
def _(nx, plt):
    # Let's set up our variables and causal relationships for this example

    # Define the complex causal DAG
    complex_graph = nx.DiGraph([
        ("B", "D"),
        ("C", "D"),
        ("A", "E"),
        ("D", "E"),
        ("A", "F"),
        ("E", "F"),
        ("D", "F")
    ])

    # Draw the DAG
    plt.rcParams['figure.figsize'] = (8, 6)
    nx.draw_networkx(complex_graph,
                     nx.spring_layout(complex_graph, seed=3),
                     with_labels=True,
                     node_color='lightblue', node_size=3000,
                     font_size=14, font_weight='bold',
                     arrows=True, arrowsize=20)
    plt.title("Causal DAG: Complex Example")
    plt.axis('off')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b> Let's say you've got a dataset with columns A-F and with a data scientist and a domain expert on your team, you construct the above DAG to represent the causal relationships between these variables.

    If you wanted to understand the causal relationship between C and E, would you need to control for any covariates?
    </b>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You wouldn't have to control for any
    """)
    return


@app.cell
def _(np, pd):
    # Let's generate data for the C->D->E subgraph to verify
    np.random.seed(456)
    B = np.random.normal(loc=100, scale=20, size=100000)
    C = np.random.binomial(1, p=0.3, size=100000)
    D = 2 * B + 0.5 * C + np.random.normal(0, 5, size=100000)

    data_3 = pd.DataFrame({"B": B, "C": C, "D": D})
    data_3.head()
    return


if __name__ == "__main__":
    app.run()
