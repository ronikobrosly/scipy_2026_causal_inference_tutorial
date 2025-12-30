# /// script
# dependencies = [
#     "causalimpact",
#     "marimo",
#     "matplotlib",
#     "numpy",
#     "pandas",
#     "tensorflow",
#     "tensorflow-probability",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Notebook 4 - Introduction to CausalImpact for Time Series

    In this notebook we'll explore the TFP CausalImpact library, a powerful Python package for measuring the causal effect of interventions on time series data. CausalImpact is particularly useful when you can't run a randomized controlled experiment but still want to understand the impact of a specific intervention or event.

    CausalImpact uses Bayesian structural time series models to answer questions like:
    - Did our marketing campaign increase sales?
    - What was the impact of a policy change on website traffic?
    - How did a product feature launch affect user engagement?

    The key idea: use control time series (unaffected by the intervention) to predict what *would have happened* to the treated time series if the intervention hadn't occurred. Then compare this counterfactual prediction to what actually happened.
    """)
    return


@app.cell
def _():
    # Import necessary libraries
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from causalimpact import fit_causalimpact
    import warnings
    warnings.filterwarnings('ignore')

    return fit_causalimpact, np, pd, plt, warnings


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Scenario: E-commerce Marketing Campaign

    Imagine you're a data analyst at an e-commerce company. Your marketing team launched a new email marketing campaign on June 1st targeting customers in the United States. They want to know: **Did the campaign actually increase daily sales?**

    The challenge: you can't randomly assign days to "campaign" vs "no campaign" - the campaign already happened! This is a classic use case for CausalImpact.

    **Your data includes:**
    - **Daily sales in the US** (treated region - received the campaign)
    - **Daily sales in Canada** (control region - didn't receive the campaign)
    - **Daily sales in the UK** (another control region)
    - **Daily website traffic** (a covariate that might help predict sales)

    The idea: Canada and UK sales, plus website traffic, can help us predict what US sales *would have been* without the campaign. The difference between this prediction and actual US sales is the causal impact!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Generate Synthetic Data

    Let's create a realistic simulated dataset. In a real analysis, you'd load your actual data.

    We'll simulate 90 days of data:
    - Days 1-60: Pre-intervention period (before the campaign)
    - Days 61-90: Post-intervention period (during the campaign)
    """)
    return


@app.cell
def _(np, pd):
    # Set random seed for reproducibility
    np.random.seed(42)

    # Number of days
    n_days = 90
    dates = pd.date_range(start='2024-03-01', periods=n_days, freq='D')

    # Generate control variables (not affected by intervention)
    # Canada sales: some trend and seasonality
    canada_trend = np.linspace(1000, 1200, n_days)
    canada_seasonal = 100 * np.sin(2 * np.pi * np.arange(n_days) / 7)  # Weekly pattern
    canada_sales = canada_trend + canada_seasonal + np.random.normal(0, 50, n_days)

    # UK sales: correlated with Canada but different scale
    uk_trend = np.linspace(800, 900, n_days)
    uk_seasonal = 80 * np.sin(2 * np.pi * np.arange(n_days) / 7)
    uk_sales = uk_trend + uk_seasonal + np.random.normal(0, 40, n_days)

    # Website traffic: another useful predictor
    traffic = np.linspace(5000, 6000, n_days) + np.random.normal(0, 200, n_days)

    # US sales (treated): correlated with controls before intervention
    # After intervention (day 60), there's a +200 boost from the campaign
    us_base = 0.8 * canada_sales + 0.4 * uk_sales + 0.05 * traffic
    intervention_effect = np.concatenate([
        np.zeros(60),  # No effect before day 60
        np.full(30, 200)  # +200 effect after day 60
    ])
    us_sales = us_base + intervention_effect + np.random.normal(0, 60, n_days)

    # Create DataFrame
    data = pd.DataFrame({
        'us_sales': us_sales,
        'canada_sales': canada_sales,
        'uk_sales': uk_sales,
        'traffic': traffic
    }, index=dates)

    data.head(10)
    return (
        canada_sales,
        canada_seasonal,
        canada_trend,
        data,
        dates,
        intervention_effect,
        n_days,
        traffic,
        uk_sales,
        uk_seasonal,
        uk_trend,
        us_base,
        us_sales,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's visualize the data to get a sense of the patterns:
    """)
    return


@app.cell
def _(data, plt):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    # US sales
    axes[0, 0].plot(data.index, data['us_sales'], color='steelblue', linewidth=2)
    axes[0, 0].axvline(x=data.index[60], color='red', linestyle='--', label='Campaign Start')
    axes[0, 0].set_title('US Sales (Treated)', fontsize=14, fontweight='bold')
    axes[0, 0].set_ylabel('Daily Sales ($)', fontsize=12)
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)

    # Canada sales
    axes[0, 1].plot(data.index, data['canada_sales'], color='darkgreen', linewidth=2)
    axes[0, 1].axvline(x=data.index[60], color='red', linestyle='--', label='Campaign Start')
    axes[0, 1].set_title('Canada Sales (Control)', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('Daily Sales ($)', fontsize=12)
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)

    # UK sales
    axes[1, 0].plot(data.index, data['uk_sales'], color='purple', linewidth=2)
    axes[1, 0].axvline(x=data.index[60], color='red', linestyle='--', label='Campaign Start')
    axes[1, 0].set_title('UK Sales (Control)', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('Daily Sales ($)', fontsize=12)
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.3)

    # Website traffic
    axes[1, 1].plot(data.index, data['traffic'], color='orange', linewidth=2)
    axes[1, 1].axvline(x=data.index[60], color='red', linestyle='--', label='Campaign Start')
    axes[1, 1].set_title('Website Traffic (Control)', fontsize=14, fontweight='bold')
    axes[1, 1].set_ylabel('Daily Visitors', fontsize=12)
    axes[1, 1].legend()
    axes[1, 1].grid(alpha=0.3)

    plt.tight_layout()
    plt.show()
    return axes, fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice how US sales appears to jump up after the red line (campaign start), while the control regions follow their usual patterns. But is this difference statistically significant? That's what CausalImpact will help us determine!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: Define the Time Periods

    CausalImpact requires us to define two periods:
    - **Pre-period**: Before the intervention (used to learn the relationship between treated and control series)
    - **Post-period**: After the intervention (used to measure the causal effect)

    For our campaign that started on day 61 (June 1st), we'll use:
    - Pre-period: Days 1-60
    - Post-period: Days 61-90
    """)
    return


@app.cell
def _(data):
    # Define the pre and post intervention periods
    pre_period = [data.index[0], data.index[59]]  # Days 1-60
    post_period = [data.index[60], data.index[89]]  # Days 61-90

    print(f"Pre-intervention period: {pre_period[0].strftime('%Y-%m-%d')} to {pre_period[1].strftime('%Y-%m-%d')}")
    print(f"Post-intervention period: {post_period[0].strftime('%Y-%m-%d')} to {post_period[1].strftime('%Y-%m-%d')}")
    return post_period, pre_period


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3: Fit the CausalImpact Model

    Now comes the exciting part! We'll use the `fit_causalimpact()` function to:
    1. Learn the relationship between US sales and the control variables during the pre-period
    2. Predict what US sales would have been in the post-period (the counterfactual)
    3. Compare the prediction to actual US sales to estimate the causal impact

    The model uses a Bayesian structural time series approach, which allows it to capture trends, seasonality, and the relationship with control variables.
    """)
    return


@app.cell
def _(data, fit_causalimpact, post_period, pre_period):
    # Fit the CausalImpact model
    # The first column is the treated series (us_sales)
    # The remaining columns are control series
    impact = fit_causalimpact(data, pre_period, post_period)

    # Display summary
    print(impact.summary())
    return (impact,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4: Interpret the Results

    The summary output tells us several important things:

    **Average Results (Posterior Inference):**
    - **Actual**: The average actual US sales during the post-period
    - **Prediction (s.d.)**: What the model predicted US sales would have been without the campaign (with standard deviation)
    - **95% CI**: The 95% credible interval for the prediction
    - **Absolute effect (s.d.)**: The difference between actual and predicted (this is our estimated causal impact!)
    - **Relative effect**: The percentage change from the predicted baseline

    **Cumulative Results:**
    - Shows the total impact over the entire post-period (all 30 days)

    **Statistical Significance:**
    - **Posterior tail-area probability p**: The probability of observing an effect this large by chance
    - **Posterior prob. of causal effect**: The probability that the campaign had a real effect

    In our simulated example, we should see a significant positive effect of approximately $200 per day, which matches the true effect we simulated!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5: Visualize the Results

    CausalImpact provides excellent built-in visualizations. Let's create them:
    """)
    return


@app.cell
def _(impact):
    # Plot the results
    impact.plot()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The plot shows three panels:

    1. **Original (top)**:
       - Black line: Actual US sales
       - Dashed line: Predicted counterfactual (what would have happened without the campaign)
       - Blue shaded area: 95% credible interval

    2. **Pointwise (middle)**:
       - Shows the difference between actual and predicted at each time point
       - This is the causal effect over time

    3. **Cumulative (bottom)**:
       - Shows the cumulative effect over time
       - Useful for understanding the total impact of the intervention

    The key insight: after the intervention, actual sales (black line) are consistently higher than predicted sales (dashed line), indicating a positive causal effect!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## When to Use CausalImpact

    CausalImpact is ideal when:
    - You have **time series data** (measurements over time)
    - You have a **clear intervention point** (when something changed)
    - You have **control time series** that weren't affected by the intervention
    - You **can't run a randomized experiment** (the intervention already happened)

    Common use cases:
    - Marketing campaign impact
    - Policy change evaluation
    - Product feature launches
    - Pricing changes
    - Regional interventions (treatment in one region, controls in others)

    **Important assumptions:**
    - The control series must not be affected by the intervention
    - The relationship between treated and control series should be stable (same in pre and post periods, except for the intervention effect)
    - You need enough pre-intervention data to learn the relationships
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 6: Working with Real Data - A Complete Example

    Let's walk through another example with a different scenario to solidify your understanding.

    **Scenario**: A streaming service added a new recommendation algorithm on week 20. Did it increase weekly hours watched?

    We'll use:
    - **Treated**: Weekly hours watched in the US
    - **Controls**: Weekly hours watched in two similar content categories that didn't get the new algorithm
    """)
    return


@app.cell
def _(np, pd):
    # Generate weekly data for 40 weeks
    np.random.seed(123)
    n_weeks = 40

    # Create weekly time index
    weeks = pd.date_range(start='2024-01-07', periods=n_weeks, freq='W')

    # Control series: content category 1 and 2 (not affected by algorithm)
    category1_base = np.linspace(10000, 12000, n_weeks)
    category1 = category1_base + np.random.normal(0, 500, n_weeks)

    category2_base = np.linspace(8000, 9500, n_weeks)
    category2 = category2_base + np.random.normal(0, 400, n_weeks)

    # Treated series: US hours watched (affected by algorithm starting week 20)
    us_base_2 = 1.5 * category1 + 0.8 * category2
    algorithm_effect = np.concatenate([
        np.zeros(19),  # No effect for weeks 1-19
        np.full(21, 3000)  # +3000 hours effect for weeks 20-40
    ])
    us_hours = us_base_2 + algorithm_effect + np.random.normal(0, 800, n_weeks)

    # Create DataFrame
    streaming_data = pd.DataFrame({
        'us_hours': us_hours,
        'category1_hours': category1,
        'category2_hours': category2
    }, index=weeks)

    streaming_data.head()
    return (
        algorithm_effect,
        category1,
        category1_base,
        category2,
        category2_base,
        n_weeks,
        streaming_data,
        us_base_2,
        us_hours,
        weeks,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b>Analyze the streaming data to estimate the causal impact of the new recommendation algorithm. Follow these steps:</b>

    1. Define the pre-period (weeks 1-19) and post-period (weeks 20-40)
    2. Fit a CausalImpact model
    3. Print the summary
    4. Create the visualization plots
    5. Interpret the results: Did the algorithm increase hours watched? By how much?
    """)
    return


@app.cell
def _(__________, streaming_data):
    # Define periods
    pre_period_stream = [streaming_data.index[0], __________]
    post_period_stream = [__________, streaming_data.index[39]]

    # Fit the model
    impact_streaming = __________(__________, __________, __________)

    # Print summary
    print(__________)
    return impact_streaming, post_period_stream, pre_period_stream


@app.cell
def _(__________):
    # Visualize results
    __________
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Great! You should see that the new algorithm caused an increase of approximately 3,000 hours per week in viewing time, which is exactly what we simulated. The cumulative effect over the 21-week post-period is around 63,000 hours!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Advanced Topic: Accessing Individual Predictions

    Sometimes you want to work with the model's predictions directly rather than just the summary. The CausalImpact object stores detailed results:
    """)
    return


@app.cell
def _(impact):
    # Access the inferences DataFrame
    inferences = impact.inferences

    # This contains columns like:
    # - 'actual': observed values
    # - 'preds': predicted counterfactual values
    # - 'preds_lower', 'preds_upper': credible interval bounds
    # - 'point_effects': pointwise causal effects
    # - 'point_effects_lower', 'point_effects_upper': effect credible intervals

    print("Available columns:", inferences.columns.tolist())
    print("\nFirst few rows of post-period:")
    print(inferences.loc[inferences.index >= '2024-04-30'].head())
    return (inferences,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This detailed output allows you to:
    - Create custom visualizations
    - Export results for reporting
    - Perform additional analyses
    - Check model fit in the pre-period
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Takeaways

    In this notebook, we've learned how to use TFP CausalImpact for time series causal inference:

    1. **Setup**: Import the library and prepare time-indexed data with treated and control series
    2. **Define periods**: Specify pre-intervention and post-intervention periods
    3. **Fit the model**: Use `fit_causalimpact()` to estimate the counterfactual
    4. **Interpret results**: Examine summary statistics and credible intervals
    5. **Visualize**: Use built-in plots to communicate findings

    **Remember:**
    - CausalImpact is powerful but relies on the assumption that control series weren't affected by the intervention
    - Good control series are key to accurate estimates
    - The model needs sufficient pre-intervention data to learn patterns
    - Always visualize your data before and after analysis
    - The credible intervals give you a sense of uncertainty in the estimates

    **Compared to other methods:**
    - **Notebook 1 (Causal Graphs)**: Helped us think about confounding in general settings
    - **Notebook 2 (S-learner)**: Used ML to estimate treatment effects with cross-sectional data
    - **Notebook 3 (DoWhy)**: Provided a formal framework for causal inference with graphs
    - **Notebook 4 (CausalImpact)**: Specialized for time series intervention analysis

    Each tool has its place depending on your data structure and research question!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bonus Exercise: Think About Your Own Data

    Consider a scenario from your work or research where CausalImpact might be useful:
    - What's the intervention you'd want to study?
    - What's your treated time series?
    - What control time series could you use?
    - How would you define the pre and post periods?

    Thinking through these questions will help you apply CausalImpact to real problems!
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
