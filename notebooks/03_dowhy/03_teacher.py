# /// script
# dependencies = [
#     "dowhy",
#     "marimo",
#     "matplotlib",
#     "numpy",
#     "pandas",
#     "scikit-learn",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Notebook 3 - Introduction to DoWhy

    In this notebook we'll explore the DoWhy library, a powerful Python package for causal inference. DoWhy provides a unified interface for causal inference methods and emphasizes the importance of making causal assumptions explicit.

    DoWhy follows a simple four-step process:
    1. **Model** the causal problem using a graph
    2. **Identify** the causal effect using graph-based criteria
    3. **Estimate** the causal effect using statistical methods
    4. **Refute** the estimate to test its robustness
    """)
    return


@app.cell
def _():
    # Import necessary libraries
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from dowhy import CausalModel
    import warnings
    warnings.filterwarnings('ignore')

    return CausalModel, np, pd, plt, warnings


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Scenario: Workplace Wellness Program

    Imagine you work as a data analyst at a mid-sized tech company. Your company recently launched a voluntary wellness program that includes:
    - Weekly fitness classes
    - Nutrition counseling
    - Stress management workshops
    - Health screenings

    The HR department wants to know: **Does participation in the wellness program actually improve employee health outcomes?**

    You have access to a dataset where each row represents an employee, with the following variables:
    - **wellness_program**: Binary indicator (1 if employee participated, 0 otherwise)
    - **health_score_change**: Change in health score over 6 months (positive = improvement)
    - **age**: Employee age in years
    - **initial_health**: Initial health score (0-100 scale)
    - **job_stress**: Job stress level (1-10 scale)
    - **tenure**: Years at the company
    - **department**: Which department the employee works in
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's start by creating a simulated dataset for this scenario. In a real analysis, you'd load your actual data.
    """)
    return


@app.cell
def _(np, pd):
    # Set random seed for reproducibility
    np.random.seed(42)
    n_samples = 1000

    # Generate synthetic data
    # Confounders
    age = np.random.normal(35, 10, n_samples)
    initial_health = np.random.normal(65, 15, n_samples)
    job_stress = np.random.randint(1, 11, n_samples)
    tenure = np.random.exponential(5, n_samples)
    department = np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR'], n_samples)

    # Treatment assignment (influenced by confounders)
    # Younger, initially healthier employees are more likely to join
    treatment_prob = 1 / (1 + np.exp(-(-2 + 0.05 * (age - 35) + 0.02 * (initial_health - 65) - 0.1 * job_stress)))
    wellness_program = np.random.binomial(1, treatment_prob, n_samples)

    # Outcome (influenced by treatment and confounders)
    health_score_change = (
        5 * wellness_program +  # Treatment effect
        -0.2 * (age - 35) +  # Older employees improve less
        -0.15 * (initial_health - 65) +  # Those starting healthier improve less
        -0.5 * job_stress +  # Stress reduces improvement
        np.random.normal(0, 3, n_samples)  # Random noise
    )

    # Create DataFrame
    data = pd.DataFrame({
        'wellness_program': wellness_program,
        'health_score_change': health_score_change,
        'age': age,
        'initial_health': initial_health,
        'job_stress': job_stress,
        'tenure': tenure,
        'department': department
    })

    data.head()
    return data, n_samples


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Model the Causal Problem

    The first step in DoWhy is to specify the causal graph. Based on domain knowledge, we believe:
    - Age, initial health status, and job stress affect both who joins the program AND health outcomes (confounders)
    - Tenure might affect who joins but doesn't directly affect health changes
    - Department doesn't affect either (just included for completeness)

    In DoWhy, we can specify the causal graph using a GML (Graph Modeling Language) string or by specifying just the confounders.
    """)
    return


@app.cell
def _(CausalModel, data):
    # Define the causal graph
    # We'll specify the confounding variables and let DoWhy handle the rest
    causal_graph = """
    digraph {
        wellness_program [label="Wellness Program"];
        health_score_change [label="Health Score Change"];
        age [label="Age"];
        initial_health [label="Initial Health"];
        job_stress [label="Job Stress"];
        tenure [label="Tenure"];

        age -> wellness_program;
        age -> health_score_change;
        initial_health -> wellness_program;
        initial_health -> health_score_change;
        job_stress -> wellness_program;
        job_stress -> health_score_change;
        tenure -> wellness_program;
        wellness_program -> health_score_change;
    }
    """

    # Create the causal model
    model = CausalModel(
        data=data,
        treatment='wellness_program',
        outcome='health_score_change',
        graph=causal_graph
    )

    return causal_graph, model


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's visualize the causal graph we've specified:
    """)
    return


@app.cell
def _(model):
    # View the causal graph
    model.view_model()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The graph clearly shows the confounding structure: age, initial_health, and job_stress each have arrows pointing to both the treatment (wellness_program) and the outcome (health_score_change). This is classic confounding!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: Identify the Causal Effect

    DoWhy will now identify the causal effect using graph-based identification methods. The most common approach is the **backdoor criterion**, which identifies confounders that need to be controlled for.
    """)
    return


@app.cell
def _(model):
    # Identify the causal effect
    identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
    print(identified_estimand)
    return (identified_estimand,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    DoWhy has identified that we need to control for the backdoor paths. The estimand tells us that to estimate the causal effect, we should adjust for the confounders: age, initial_health, and job_stress.

    This matches our intuition from the causal graph!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3: Estimate the Causal Effect

    Now comes the fun part - actually estimating the causal effect! DoWhy supports many estimation methods. We'll try a few:

    1. **Backdoor methods** (like propensity score matching, linear regression)
    2. **Instrumental variable methods** (when we have instruments)
    3. **Regression discontinuity** (when there's a threshold)

    For our case, we'll use backdoor methods since we have identified confounders.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Method 1: Linear Regression (Backdoor Adjustment)

    This is the most straightforward approach - we'll regress the outcome on the treatment and confounders.
    """)
    return


@app.cell
def _(identified_estimand, model):
    # Estimate using linear regression
    estimate_lr = model.estimate_effect(
        identified_estimand,
        method_name="backdoor.linear_regression",
        test_significance=True
    )

    print(estimate_lr)
    return (estimate_lr,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The estimated causal effect is approximately 5 points on the health score scale. This means that participating in the wellness program causes an average improvement of about 5 points in health scores over 6 months.

    Since we simulated this data, we know the true effect is exactly 5 - so our estimate is quite good!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Method 2: Propensity Score Matching

    Propensity score matching is another popular method. It matches treated and control units with similar probabilities of receiving treatment.
    """)
    return


@app.cell
def _(identified_estimand, model):
    # Estimate using propensity score matching
    estimate_psm = model.estimate_effect(
        identified_estimand,
        method_name="backdoor.propensity_score_matching"
    )

    print(estimate_psm)
    return (estimate_psm,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The propensity score matching estimate is also close to 5! Different methods can give slightly different estimates, but they should generally agree if our assumptions are correct.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b>Try estimating the effect using propensity score stratification. Use `method_name="backdoor.propensity_score_stratification"`. How does it compare to the other estimates?</b>
    """)
    return


@app.cell
def _(identified_estimand, model):
    # Estimate using propensity score stratification
    estimate_pss = model.estimate_effect(
        identified_estimand,
        method_name="backdoor.propensity_score_stratification"
    )

    print(estimate_pss)
    return (estimate_pss,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4: Refute the Estimate

    This is where DoWhy really shines! We can test the robustness of our estimate using various refutation tests. These tests help us check whether our causal assumptions hold.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Refutation Test 1: Random Common Cause

    This test adds a randomly generated confounder to the data and re-estimates. If our estimate changes significantly, it suggests we might be missing important confounders.
    """)
    return


@app.cell
def _(estimate_lr, model):
    # Refute by adding a random common cause
    refute_random = model.refute_estimate(
        estimate_lr,
        method_name="random_common_cause"
    )

    print(refute_random)
    return (refute_random,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Good news! The estimate doesn't change much when we add a random confounder. The new effect is close to the original, which suggests our model is reasonably robust.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Refutation Test 2: Placebo Treatment

    This test replaces the treatment with a random variable. If we still see a significant effect, something is wrong with our analysis!
    """)
    return


@app.cell
def _(estimate_lr, model):
    # Refute using placebo treatment
    refute_placebo = model.refute_estimate(
        estimate_lr,
        method_name="placebo_treatment_refuter",
        placebo_type="permute"
    )

    print(refute_placebo)
    return (refute_placebo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Excellent! When we use a placebo treatment (random assignment), the estimated effect drops close to zero. This is what we'd expect - it means our original effect wasn't just due to chance or model misspecification.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Refutation Test 3: Data Subset Validation

    This test checks if the estimate is stable across different subsets of the data.
    """)
    return


@app.cell
def _(estimate_lr, model):
    # Refute using data subset
    refute_subset = model.refute_estimate(
        estimate_lr,
        method_name="data_subset_refuter",
        subset_fraction=0.8
    )

    print(refute_subset)
    return (refute_subset,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The estimate remains stable when we use only 80% of the data. This suggests our result isn't driven by a small subset of unusual observations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <b>EXERCISE</b>

    <b>What happens if we analyze a subset of the data - say, only employees in the Engineering department? Does the treatment effect differ across departments?</b>

    Hint: Filter the data to only include Engineering employees, create a new causal model, and estimate the effect.
    """)
    return


@app.cell
def _(CausalModel, causal_graph, data):
    # Filter data for Engineering department
    data_eng = data[data['department'] == 'Engineering']

    # Create new causal model
    model_eng = CausalModel(
        data=data_eng,
        treatment='wellness_program',
        outcome='health_score_change',
        graph=causal_graph
    )

    # Identify and estimate
    identified_estimand_eng = model_eng.identify_effect(proceed_when_unidentifiable=True)
    estimate_eng = model_eng.estimate_effect(
        identified_estimand_eng,
        method_name="backdoor.linear_regression"
    )

    print(f"Effect in Engineering department: {estimate_eng.value:.3f}")
    return data_eng, estimate_eng, identified_estimand_eng, model_eng


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Comparing DoWhy to What We Did in Notebook 2

    In Notebook 2, we manually:
    1. Specified confounders based on domain knowledge
    2. Built a predictive model
    3. Made counterfactual predictions

    DoWhy automates and formalizes this process:
    1. The causal graph makes our assumptions **explicit** and **visualizable**
    2. The identification step uses **formal graph theory** (backdoor criterion, etc.)
    3. Multiple estimation methods are available with consistent interfaces
    4. **Refutation tests** help us validate our assumptions - this is unique to DoWhy!

    DoWhy doesn't replace domain knowledge - you still need to specify the causal graph correctly. But it provides a principled framework for causal inference.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    In this notebook, we've learned how to use DoWhy for causal inference:

    1. **Model**: Specify the causal graph based on domain knowledge
    2. **Identify**: Use graph-based methods (backdoor criterion) to identify what needs to be controlled
    3. **Estimate**: Apply various statistical methods to estimate the causal effect
    4. **Refute**: Test the robustness of our estimates using multiple refutation tests

    DoWhy's strength is in making causal assumptions explicit and providing tools to test them. The refutation framework is particularly valuable - it helps us understand when we should trust our causal estimates and when we should be skeptical.

    For your own analyses, remember:
    - The causal graph is critical - spend time thinking through it with domain experts
    - Try multiple estimation methods to check robustness
    - Always run refutation tests before making strong causal claims
    - Be humble about causal inference - it's powerful but relies on untestable assumptions
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
