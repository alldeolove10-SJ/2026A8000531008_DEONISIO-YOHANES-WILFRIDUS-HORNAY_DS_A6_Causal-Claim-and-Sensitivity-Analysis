"""
DS-A6 supporting example — synthetic tutoring data only.
Run from project root: python src/demo_causal_sensitivity.py
This is a method demonstration, NOT the completed assessed assignment.
"""
from pathlib import Path
import hashlib, json, platform, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

ROOT=Path(__file__).resolve().parents[1]
for d in ["data","results","figures"]: (ROOT/d).mkdir(exist_ok=True)
DATA=ROOT/"data"/"synthetic_tutoring_example.csv"
SEED=6042
if not DATA.exists():
    rng=np.random.default_rng(SEED); n=2400
    prior=rng.normal(65,12,n); motivation=rng.normal(0,1,n); family=rng.normal(0,1,n)
    prob=1/(1+np.exp(-(-.25+.035*(prior-65)+.65*motivation+.25*family)))
    treat=rng.binomial(1,prob,n)
    study=np.maximum(0,4+.10*(prior-65)+.9*motivation+.5*treat+rng.normal(0,1.5,n))
    exam=.62*prior+3*treat+2*motivation+.8*family+rng.normal(0,7,n)
    prequiz=.75*prior+2.5*motivation+.7*family+rng.normal(0,6,n)
    engagement=.35*treat+.12*(exam-40)+rng.normal(0,1,n)
    selected=(engagement>np.quantile(engagement,.18)).astype(int)
    pd.DataFrame({"student_id":np.arange(1,n+1),"prior_score":prior,"family_support":family,
      "tutoring":treat,"study_hours_post":study,"exam_score":exam,
      "pre_treatment_quiz":prequiz,"engagement_selection":selected}).to_csv(DATA,index=False,float_format="%.6f")
df=pd.read_csv(DATA)
sha=hashlib.sha256(DATA.read_bytes()).hexdigest()
assert df["student_id"].is_unique and df["tutoring"].isin([0,1]).all()
assert df["exam_score"].notna().all()

def fit_effect(outcome, covariates):
    model=sm.OLS(df[outcome],sm.add_constant(df[["tutoring"]+covariates],has_constant="add")).fit(cov_type="HC3")
    lo,hi=model.conf_int().loc["tutoring"]
    return {"estimate":float(model.params["tutoring"]),"se":float(model.bse["tutoring"]),
            "ci_low":float(lo),"ci_high":float(hi),"p_value":float(model.pvalues["tutoring"]),
            "n":int(model.nobs),"r2":float(model.rsquared)}
naive=fit_effect("exam_score",[])
adjusted=fit_effect("exam_score",["prior_score","family_support"])
mediator_diag=fit_effect("exam_score",["prior_score","family_support","study_hours_post"])
negative_control=fit_effect("pre_treatment_quiz",["prior_score","family_support"])
rows=[]
for label,result in [("Unadjusted association",naive),
                     ("Adjusted for measured pre-treatment covariates",adjusted),
                     ("Includes post-treatment mediator (diagnostic only)",mediator_diag),
                     ("Negative-control outcome: pre-treatment quiz",negative_control)]:
    rows.append({"analysis":label,**{k:result[k] for k in ["estimate","se","ci_low","ci_high","p_value","n","r2"]}})
results=pd.DataFrame(rows); results.to_csv(ROOT/"results"/"demo_estimates.csv",index=False)
# Transparent illustrative bias-shift analysis, not a universal sensitivity estimator.
bias=np.linspace(-4,4,81)
pd.DataFrame({"assumed_omitted_bias":bias,"bias_adjusted_effect":adjusted["estimate"]-bias,
 "ci_low":adjusted["ci_low"]-bias,"ci_high":adjusted["ci_high"]-bias}).to_csv(ROOT/"results"/"demo_omitted_bias_sensitivity.csv",index=False)

GREEN="#16803c"; PINK="#ec168c"; GRAY="#777777"
plt.rcParams.update({"font.size":9,"axes.titlesize":12,"axes.labelsize":10,"legend.fontsize":8})
fig,ax=plt.subplots(figsize=(8,4.5))
labels=["Unadjusted","Pre-treatment\nadjusted","Including mediator\n(diagnostic)"]
vals=[naive["estimate"],adjusted["estimate"],mediator_diag["estimate"]]
lo=[naive["ci_low"],adjusted["ci_low"],mediator_diag["ci_low"]]; hi=[naive["ci_high"],adjusted["ci_high"],mediator_diag["ci_high"]]
x=np.arange(3); ax.errorbar(x,vals,yerr=[np.array(vals)-lo,np.array(hi)-vals],fmt="o",capsize=5,color=GREEN,ecolor=PINK,lw=1.5)
ax.axhline(0,color=GRAY,ls="--"); ax.set_xticks(x,labels); ax.set_ylabel("Tutoring coefficient (score points)")
ax.set_title("Synthetic Example: Estimates Depend on Adjustment Set"); ax.grid(axis="y",alpha=.2)
fig.tight_layout(); fig.savefig(ROOT/"figures"/"01_demo_estimate_comparison.png",dpi=220); plt.close(fig)
sens=pd.read_csv(ROOT/"results"/"demo_omitted_bias_sensitivity.csv")
fig,ax=plt.subplots(figsize=(8,4.5)); ax.plot(sens.assumed_omitted_bias,sens.bias_adjusted_effect,color=GREEN,lw=2,label="Bias-adjusted point estimate")
ax.fill_between(sens.assumed_omitted_bias,sens.ci_low,sens.ci_high,color=PINK,alpha=.18,label="Shifted 95% CI")
ax.axhline(0,color=GRAY,ls="--"); ax.axvline(0,color=GRAY,ls=":")
ax.set(title="Illustrative Omitted-Confounding Sensitivity",xlabel="Assumed omitted-variable bias (score points)",ylabel="Adjusted effect after assumed bias")
ax.legend(); ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(ROOT/"figures"/"02_demo_sensitivity_curve.png",dpi=220); plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.5))
ax.hist(df.loc[df.tutoring==0,"exam_score"],bins=35,alpha=.55,color=GREEN,label="No tutoring")
ax.hist(df.loc[df.tutoring==1,"exam_score"],bins=35,alpha=.45,color=PINK,label="Tutoring")
ax.set(title="Outcome Distributions by Observed Treatment (Synthetic)",xlabel="Exam score",ylabel="Students")
ax.legend(); ax.grid(axis="y",alpha=.15); fig.tight_layout(); fig.savefig(ROOT/"figures"/"03_demo_outcome_distributions.png",dpi=220); plt.close(fig)
env={"purpose":"synthetic method demonstration only","seed":SEED,"python":sys.version,"platform":platform.platform(),
 "numpy":np.__version__,"pandas":pd.__version__,"statsmodels":sm.__version__,"dataset_sha256":sha,
 "n_rows":len(df),"true_treatment_effect_in_generator":3.0}
(ROOT/"results"/"demo_environment.json").write_text(json.dumps(env,indent=2),encoding="utf-8")
print("Synthetic causal demonstration completed. Data SHA-256:",sha)
print(results[["analysis","estimate","ci_low","ci_high","n"]].round(3).to_string(index=False))
print("Do not present these synthetic results as evidence about a real tutoring programme.")
