# November Intake: Payoff, Prices, Value Capture and Assessment

Inspected **26 October 2026**. Unpublished material for `codex/november-2026-preparation`; October remains closed and unchanged.

## Admission Decisions

| Suggested source | Decision and useful contribution | Boundary |
| --- | --- | --- |
| [Torsten Slok, Apollo, 24 October](https://www.apollo.com/wealth/insights-news/insights/daily-spark/no-signs-of-ai-payoff-outside-the-tech-sector) | Include as a skeptical macro-level interpretation. | Descriptive aggregates do not identify zero causal returns to adoption. |
| [Max Woolf, 25 October](https://minimaxir.com/2026/10/cheap-llms/) | Include the distinction between token prices, effective workload costs and market explanations. | Do not adopt durable price, profitability or competitive-equivalence predictions as findings. |
| [Steven Strogatz, The Atlantic, 25 October](https://www.theatlantic.com/ideas/2026/10/ai-math-human-future/689133/) | Retain as a **public-preview-only** perspective on mathematics as human practice. | Full text remains subscription-restricted. Do not summarize its complete argument or reuse numerical breakthrough claims as verified results. |
| [Audrey Baime, The Daily Californian, 23 October](https://www.dailycal.org/news/campus/academics/ai-use-leads-uc-berkeley-math-professor-to-see-no-point-in-grading-homework/article_bdf1eae2-c08b-491f-b9f1-81a7cea177de.html) | Include a reported case of assessment redesign. | One professor's practice is neither a campus-wide rule nor a measured learning effect. |
| [Reuters, inspected syndication dated 21 August](https://www.thestar.com.my/tech/tech-news/2026/08/21/ai-reshapes-india039s-it-services-sector-contracts-as-clients-demand-more-for-less) | Include contract pressure as evidence about **value capture**, based on reported interviews. | Requested discounts and promised savings are not audited, realized productivity gains. |

These are not five independent estimates of whether AI helps. Their units range from aggregate financial indicators to invoices, contracts, professional experience and assessment practices.

## Proposed Article Additions

### Section 9: Cheaper inputs, realized gains and who captures them

Slok argues that broad corporate indicators do not yet show the expected payoff outside a small group of dominant firms. That challenge belongs in the discussion, but the comparison does not identify adoption's causal effect. The S&P constituents outside the Mag 7 are not a clean non-technology sector, and aggregate margins lack a no-AI counterfactual. Neither a universal zero return nor guaranteed hidden benefits follows. [@slokpayoff2026]

Woolf highlights falling advertised token prices and the importance of caching. Primary vendor rate cards establish posted prices, not realized project returns. Vercel's gateway observations also distinguish growing estimated spend from declining average token prices; its spending series is imputed from list prices, not actual invoices. Neither platform coverage nor changing model mix permits an economy-wide, quality-adjusted savings estimate. [@woolfcheap2026; @opus55pricing2026; @vercelindex2026]

Reuters reports pressure on Indian IT-service fees and a shift toward outcome-linked arrangements. Supplier revenue compression can coexist with customer gains, but the report does not audit those gains. More work, lower prices and different contract risks need separate measurement. Announced targets are not achieved savings. [@reutersitcontracts2026]

Our synthesis is to ask **whose benefit is measured**. Lower input prices, improved delivery, supplier margins, buyer savings, worker outcomes and social value are distinct. Their relationships require evidence; one cannot substitute for another. Failed adoption must remain visible, but unchanged supplier margins alone are not a complete value test.

These sources also concern different geographies and populations. Indian IT-service contracting is not a matched counterexample to a claim about US companies outside technology, and an aggregate US comparison cannot settle the returns to a particular Indian client's deployment. The connection is conceptual, not a pooled positive-versus-negative test.

### Sections 6–7: Assessment and the human purpose of intellectual work

Baime reports Borcherds replacing correctness-based homework marking with completion credit. The case concerns whether submitted answers remain informative about understanding, not a measured decline in learning or an end to assessment. It complements, rather than replaces, experiments comparing assisted performance with unaided retention and transfer. [@baimehomework2026; @bastani2025; @bergh2026]

Strogatz's accessible opening conveys disciplinary anxiety and frames mathematics as human expression. It supplies a perspective on the purpose of mathematical work, not a validation of technical claims or evidence that the discipline has reached a settled consensus. The remainder of the essay was not inspected in full. [@strogatzfuture2026]

## Critical Reading Notes

### Apollo: the inference is stronger than the design

The article and chart captions were read, not the raw Bloomberg/Macrobond inputs or reconstructed series. The financial comparison cannot isolate AI from demand, sector composition, prices, investment timing or other changes. A utilization-adjusted productivity series also does not supply a treatment-control design for AI. Statements about judgment or culture require different evidence from financial charts. These are our methodological objections, not a claim that the reported aggregates are false. Link to the presentation; do not redistribute Apollo's charts.

### Prices: cost accounting before market forecasts

[Anthropic's dated announcement](https://www.anthropic.com/claude-opus-5-5) lists standard Opus 5.5 rates per million tokens: $4 input, $20 output, $0.20 cache reads and $5 cache writes. Those fields were checked; vendor benchmark and typical-workload savings claims were not independently evaluated. [OpenAI's linked announcement](https://openai.com/index/introducing-gpt-6-1-sol/) was also checked for selected price fields, without treating its capability claims as validated here.

For comparison, calculate API charges across the applicable token categories, including cache writes, reads and output. A share of token volume is not a share of dollars. Add retries, tool execution, verification, integration and human time to obtain total cost per accepted result. Comparisons should hold workload and required quality explicit. Subscription limits are a different pricing instrument from API rates.

[Vercel's report](https://vercel.com/blog/ai-gateway-production-index-october-2026), by Amelia Charles and Harpreet Arora, is primary platform reporting, not an independent market census. Its methods cover gateway traffic through September, estimate spending from published prices and allow historical revisions. Model mix and definition changes matter. Current rate cards and provider counts do not establish cost structure, future equilibrium prices, negligible switching friction or the absence of subsidy.

### Contracts: reported bargaining is not a treatment effect

The Reuters byline is Sai Ishwarbharath B, Abhirami G and Haripriya Suresh. The original URL was inaccessible, but attributed syndications were inspected in The Star and MarketScreener. They are one story, not replications. The Star's 21 August date and the original URL's 20 August date are recorded separately rather than silently conflated.

The reported 25–30% figure is a client's requested price reduction as described by an executive, not measured engineering acceleration. The TCS contract-share figure concerns a business-services segment, not all contracts. Some terms rely on anonymous sources or remain unconfirmed by counterparties. Predictions about entry-level staffing and future gains stay labeled as forecasts. The useful new mechanism is contractual allocation of benefits and risk, not an industry-wide causal estimate.

### Education and mathematics: what was actually inspected

Local Chrome exposed the Daily Californian's full article and the Atlantic's headline, author, date, subtitle and public opening. No subscription barrier was bypassed. The Berkeley report distinguishes the professor's remarks from reported institutional comments about faculty discretion. Neither those remarks nor Strogatz's preview establishes a general career forecast, a measured loss of competence or correctness of a mathematical proof.

This suggests a research distinction rather than a conclusion: learning, assessment validity, feedback and the meaning attached to intellectual work can change differently. Compare assessment designs and retained understanding directly; do not infer them solely from polished submitted work or a professional's reaction.

## Staging and Follow-Up

Seven records are staged in [November sources](../data/november-sources.json): the five suggestions plus primary Anthropic pricing and Vercel methodology. [Chrome observations](../november/browser-observations.json) document actual 26 October inspections for the two restricted sites; they are not November release receipts.

Before publication, refresh prices and methodological versions, recheck selected sites in the monthly browser channel, and obtain the Atlantic full text before broadening its appraisal. No source chart, subscription article, private invoice or contract is redistributed. October's generated files and release metadata are untouched.
