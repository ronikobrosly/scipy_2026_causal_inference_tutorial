# /// script
# dependencies = ["matplotlib", "pandas", "sklearn", "pydot"]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import subprocess
    return (subprocess,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Notebook 2 - Experimenting with g-computation / s-learner
    """)
    return


@app.cell
def _(subprocess):
    #! apt-get install graphviz
    subprocess.call(['apt-get', 'install', 'graphviz'])
    # packages added via marimo's package management: matplotlib pandas sklearn pydot !pip install matplotlib pandas sklearn pydot
    return


@app.cell
def _():
    from graphviz import Digraph
    import matplotlib.pyplot as plt
    import pandas as pd
    from sklearn.metrics import classification_report
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.neighbors import NearestNeighbors
    from sklearn.preprocessing import StandardScaler

    # '%matplotlib inline' command supported automatically in marimo
    return (
        Digraph,
        GradientBoostingClassifier,
        StandardScaler,
        classification_report,
        pd,
        train_test_split,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For this notebook we're going to be working with a semi-simulated dataset relating to customer churn at a cell phone company. The dataset is structured such that each row corresponds to a unique customer. We'll be working with contains the following columns:

    **customer_id**: Unique primary key for each individual in the dataset

    **region**: Which region in the United States does the customer live in?

    **acct_length**: How many days has the customer been active for?

    **internation_plan**: Does the customer have the international plan enabled?

    **voicemail_plan**: Does the customer have the voicemail plan enabled?

    **daytime_call_mins**: What is the total number of daytime call minutes the user has had?

    **evening_call_mins**: What is the total number of evening time call minutes the user has had?

    **nighttime_call_mins**: What is the total number of nighttime call minutes the user has had?

    **customer_service_calls**: How many customer service calls has the user made?

    **churn**: Did the customer quit the service?

    **age**: What is the age of the user (in years)?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The company is proposing rolling out the international plan to all customers, and increasing base plan prices across the board. To help understand the effects of this plan, they want to carry out an analysis to understand the causal effect of the international plan on the probability churn in this population. So in this case, the "treatment" is the presence of that phone plan, the outcome is the churn flag.

    As far as confounders we'll control for, let's say you have a whiteboarding session with the business team and collectively you decide the following causal DAG is a decent representation of how the variables in this dataset relate to each other:
    """)
    return


@app.cell
def _(Digraph):
    g = Digraph('churn_causality')
    g.edge('internation_plan', 'churn')
    g.edge('age', 'churn')
    g.edge('region', 'churn')
    g.edge('customer_service_calls', 'churn')
    g.edge('acct_length', 'customer_service_calls')
    g.edge('daytime_call_mins', 'acct_length')
    g.edge('evening_call_mins', 'acct_length')
    g.edge('nighttime_call_mins', 'acct_length')
    g.edge('voicemail_plan', 'churn')
    g.edge('age', 'internation_plan')
    g.edge('age', 'voicemail_plan')
    g.edge('region', 'internation_plan')
    g.edge('region', 'voicemail_plan')
    g.edge('acct_length', 'churn')
    g
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Based on this above causal DAG, there are only two obvious confounders of the international plan - churn relationship: age and region. So these are the only two covariates we'll plan on controlling for.
    """)
    return


@app.cell
def _(pd):
    df = pd.read_csv("https://raw.githubusercontent.com/ronikobrosly/misc_dataset/main/causal_churn.csv")
    df.head()
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### First, let's clean up the data a bit
    """)
    return


@app.cell
def _(StandardScaler, df):
    # Let's scale our continuous or close to continuous covariates
    features = df[['acct_length', 'daytime_call_mins', 'evening_call_mins', 'nighttime_call_mins', 'age']]

    # Use scaler of choice; here Standard scaler is used
    scaler = StandardScaler().fit(features.values)
    features = scaler.transform(features.values)

    df[['acct_length', 'daytime_call_mins', 'evening_call_mins', 'nighttime_call_mins', 'age']] = features
    return


@app.cell
def _(df, pd):
    # We'll convert the `region`, `internation_plan`, `voicemail_plan`, and `customer_service_calls` columns into categorical columns

    df2 = pd.concat(
        [
            df[["churn", "age", "acct_length", "daytime_call_mins", "evening_call_mins", "nighttime_call_mins"]],
            pd.get_dummies(df["region"], prefix = "region"),
            pd.get_dummies(df["internation_plan"], prefix = "int_plan"),
            pd.get_dummies(df["voicemail_plan"], prefix = "vm_plan"),
            pd.qcut(df['customer_service_calls'], 2, labels=[0, 1]) # let's just split this at the median (low vs high)
        ],
        axis = 1
    )
    return (df2,)


@app.cell
def _(df2):
    # Now we can drop necessary columns (i.e. one reference column from each dummy variable group)
    df2.drop(columns = ["region_East North Central", "int_plan_no", "vm_plan_no"], inplace = True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### First, let's train a predictive model with scikit-learn. This model should take in the treatment variable and covariates, and predict the outcome variable (i.e. `churn`)

    If you're curious about how well the model performs that's probably a good thing to be curious about. Let's split our small dataset into test and training sets. Now, admittedly, we have a tiny dataset, but we're doing this to show that standard ML evaluation methods are still relevant here.
    """)
    return


@app.cell
def _(df2, train_test_split):
    train_df, test_df = train_test_split(df2, test_size = 0.25, random_state = 512)
    return test_df, train_df


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can use any sort of model you'd like (from simple linear ones to very complex ones)
    """)
    return


@app.cell
def _():
    features_1 = ['age', 'region_East South Central', 'region_Middle Atlantic', 'region_Mountain', 'region_New England', 'region_Pacific', 'region_South Atlantic', 'region_West North Central', 'region_West South Central', 'int_plan_yes']
    return (features_1,)


@app.cell
def _(GradientBoostingClassifier, features_1, train_df):
    temp_model = GradientBoostingClassifier(random_state=512).fit(X=train_df[features_1], y=train_df['churn'])
    return (temp_model,)


@app.cell
def _(classification_report, features_1, temp_model, test_df):
    print(classification_report(y_true=temp_model.predict(test_df[features_1]).reshape(-1, 1), y_pred=test_df['churn'].values.reshape(-1, 1)))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You could compare different model types here to see which performs best in your hold-out set. As you might expect, you'll want a model that performs well for both classes, so that we can make good inferences.

    The metrics for the "churned" class in this example look awful (even if the overall model accuracy seems good on the surface), however, because this is just a demonstration so we'll continue moving forward. Let's now train on the whole dataset.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b> Train a classification model using the full set of data (training + test sets combined). </b>
    """)
    return


@app.cell
def _(GradientBoostingClassifier, _________):
    model = GradientBoostingClassifier(_________)
    return (model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Now that we have a model we can start making predictions to see counterfactual outcomes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b> Take the full dataset and "force" everyone to have received the treatment, what is the mean probability of all individuals to have churned? </b>
    """)
    return


@app.cell
def _(_______):
    df_treat = _______
    return


@app.cell
def _(__________, model):
    # Let's get the probability of churn from these predictions
    treat_churn_prob = model.predict_proba(__________)
    print(f"Mean probability of churning in this hypothetical treatment population is {round(treat_churn_prob, 3)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b> Take the full dataset and "force" everyone to have NOT received the treatment, what is the mean probability of all individuals to have churned? </b>
    """)
    return


@app.cell
def _(_______):
    df_ctrl = _______
    return


@app.cell
def _(________, model):
    # Let's get the probability of churn from these predictions
    ctrl_churn_prob = model.predict_proba(________)
    print(f"Mean probability of churning in this hypothetical control population is {round(ctrl_churn_prob, 3)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## This is a very interesting outcome. Essentially you found that enabling international calls across the board (as well as increasing the base phone plan rate to account for this), increases the probability of churning in this population by about 239% (11.7% to 39.7%)! You can think of this delta as your average treatment effect (ATE).

    Now remember, one of the challenges of causal inference is with what we have at our disposal, we have no way of determining if this is correct. So there are a few possibilities at this point:

    1) We took all of the relevant data, correctly specified the causal DAG, picked the correct confounding variables to control for, and rolling out this intervention (everyone gets ability to make international calls and also sees an increase in their base phone plan price) to the whole population will cause a big uptick in churn.

    2) We have all of the relevant data, and have incorrectly specified our causal DAG and as a result picked a wrong set of covariates to control for. Better re-assess this with the domain experts.

    3) We're missing critical variables in our dataset and there is unaccounted for confounding bias going on here. Can you try to brainstorm what these could be and see if you're able to bring in that data?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## You could obtain confidence intervals around this estimate by taking bootstrap replicates of the original dataset, training a new model on each replicate, and then calculating the ATE for each replicate. The 2.5th and 97.5th percentiles of these values would represent the bounds of your 95% confidence interval.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b> Can you calculate the average treatment effect among the treated (ATT)? Hint: just as the metric's name suggests, you would focus exclusively on the originally treated group, and see how a receiving and not receiving the treatment among that group would play out. </b>
    """)
    return


@app.cell
def _(_________, __________):
    df_treat_1 = _________
    treat_churn_prob_1 = __________
    print(f'Mean probability of churning in this hypothetical treatment population is {round(treat_churn_prob_1, 3)}')
    return


@app.cell
def _(_________):
    df_ctrl_1 = _________
    ctrl_churn_prob_1 = _________
    print(f'Mean probability of churning in this hypothetical treatment population is {round(ctrl_churn_prob_1, 3)}')
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()

