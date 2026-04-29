# RAG Evaluation Results

**Student:** Anay Abhijit Joshi  
**Student ID:** 904168649  
**Embedding model:** `BAAI/bge-small-en-v1.5`  
**LLM:** `llama3.2:3b` via ollama  
**Top-k retrieved per query:** 8

Each ticker has 2 manual test questions, run against two different fiscal years (2018 and 2015) to demonstrate that metadata filtering works across the full year range. For each question we show the question, the **highest-ranked retrieved chunk** (truncated), and the **generated answer**.


---

## AFL

### Question 1 -- Fiscal Year 2018

**Q:** What are Aflac's primary insurance product lines and in which geographic markets does the company operate?

**Top retrieved chunk (truncated to 600 chars):**

```
THE COMPANY'S BUSINESS

 Aflac Incorporated (the Parent Company) and its subsidiaries (collectively, the Company) primarily sell supplemental health and life insurance in the United States and Japan. The Company's insurance business is marketed and administered through American Family Life Assurance Company of Columbus (Aflac) in the United States (Aflac U.S.) and, effective April 1, 2018, through Aflac Life Insurance Japan Ltd. in Japan (Aflac Japan). Prior to April 1, 2018, the Company's insurance business was marketed in Japan as a branch of Aflac. (For more information about the conversion
```

**Generated answer:**

Aflac's primary insurance product lines include:

1. Accident insurance
2. Cancer insurance
3. Critical care insurance
4. Income support
5. Hospital indemnity insurance
6. Dental insurance
7. Life insurance
8. Vision insurance
9. Protection (including term and whole life insurance)
10. Child endowment

Aflac operates in two geographic markets:

1. The United States (Aflac U.S.)
2. Japan (Aflac Japan)

### Question 2 -- Fiscal Year 2015

**Q:** What were the principal risk factors disclosed by Aflac, and how does foreign currency exposure affect its results?

**Top retrieved chunk (truncated to 600 chars):**

```
For more information regarding interest rate risk, see the Interest Rate Risk subsection within the Market Risks of Financial Instruments section of MD&A in this report.

 Our concentration of business in Japan poses risks to our operations.
 Our operations in Japan, including realized gains and losses on Aflac Japan's investment portfolio, accounted for 70% of our total revenues for 2015 , compared with 72% in 2014 and 74% in 2013 . The Japanese operations accounted for 83% of our total assets at December 31, 2015 , compared with 82% at December 31, 2014 .

 Further, because of the concentrat
```

**Generated answer:**

The principal risk factors disclosed by Aflac include:

1. Concentration of business in Japan, which poses risks to operations.
2. Material exposure to the Japanese economy, geo-political climate, political regime, and other factors that generally determine a country's creditworthiness.
3. Limited availability of acceptable yen-denominated investments.
4. Foreign currency fluctuations in the yen/dollar exchange rate.

Foreign currency exposure affects Aflac's results as follows:

* Yen-denominated income statement accounts are translated to U.S. dollars using a weighted-average Japanese yen/U.S. dollar foreign exchange rate, while yen-denominated balance sheet accounts are translated to U.S. dollars using a spot Japanese yen/U.S. dollar foreign exchange rate.
* Changes in the yen/dollar exchange rate can affect the value of Aflac's investments and liabilities, leading to unrealized foreign currency translation adjustments reported in accumulated other comprehensive income.
* Foreign currency fluctuations can impact the computation of Aflac Japan's risk-based capital ratio due to its consolidation with the U.S. statutory filings.
* The yen strengthening has the effect of suppressing current year results in relation to the prior year, while yen weakening has the effect of magnifying current year results in relation to the prior year.
* Foreign currency translation also impacts the earnings volatility of Aflac Japan's comprehensive income due to its exposure to U.S. interest rates and credit spreads through its hedging program.


---

## CAT

### Question 1 -- Fiscal Year 2018

**Q:** What are Caterpillar's main reporting segments and what products or services does each segment provide?

**Top retrieved chunk (truncated to 600 chars):**

```
Construction Industries	$	8,742	$	1,396	$	3,760	$	5,235	$	19,133	$	107	$	19,240
Resource Industries	2,582	1,281	1,775	1,866	7,504	357	7,861
Energy & Transportation	7,959	1,261	4,431	2,313	15,964	3,418	19,382
All Other Segments	70	3	54	51	178	392	570
Corporate Items and Eliminations	(97	)	(1	)	(6	)	1	(103	)	(4,274	)	(4,377	)
Machinery, Energy & Transportation	19,256	3,940	10,014	9,466	42,676	—	42,676
Financial Products Segment	2,006	306	418	363	3,093	—	3,093
Corporate Items and Eliminations	(190	)	(46	)	(19	)	(52	)	(307	)	—	(307	)
Financial Products Revenues	1,816	260	399	311	2,786	—	2,786
Cons
```

**Generated answer:**

Caterpillar's three primary reporting segments are:

1. Machinery, Energy & Transportation - This segment includes Construction Industries, Resource Industries, Energy & Transportation, and All Other operating segments and related corporate items and eliminations.
   Caterpillar manufactures construction equipment, mining equipment, diesel engines, industrial gas turbines, locomotives, and other products.

2. Financial Products - This segment primarily includes the company's Financial Products Segment.
   Caterpillar provides financing for users of its products through various competitive sources, including commercial banks and finance and leasing companies.

3. All Other Segments - This segment is not further specified in the provided context.

These segments provide a range of products and services, including construction equipment, mining equipment, diesel engines, industrial gas turbines, locomotives, financing options for customers, and other related products and services.

### Question 2 -- Fiscal Year 2015

**Q:** How does Caterpillar describe the seasonality and cyclical nature of demand for its construction and mining equipment?

**Top retrieved chunk (truncated to 600 chars):**

```
The chart above graphically illustrates reasons for the change in Consolidated Sales and Revenues between 2013 (at left) and 2014 (at right). Items favorably impacting sales and revenues appear as upward stair steps with the corresponding dollar amounts above each bar, while items negatively impacting sales and revenues appear as downward stair steps with dollar amounts reflected in parentheses above each bar. Caterpillar management utilizes these charts internally to visually communicate with the company's Board of Directors and employees.

 Total sales and revenues were $55.184 billion in 20
```

**Generated answer:**

Caterpillar describes the seasonality and cyclical nature of demand for its construction and mining equipment by stating that dealers adjust inventory levels based on their expectations of future demand and product delivery times. They also mention that customers reduce capital expenditures during periods of weak economic growth or when commodity prices are low, which can lead to lower end-user demand for mining equipment.


---

## IBM

### Question 1 -- Fiscal Year 2018

**Q:** What are IBM's main business segments and which segment contributes the largest share of revenue?

**Top retrieved chunk (truncated to 600 chars):**

```
Segment
information and revenue by classes of similar products or servicespages 141 to 146.

 Financial
information regarding environmental activitiespage 111.

 The
number of persons employed by the registrantpage 67.

 The
management discussion overviewpages 19 to 21.

 Website
information and company reportingpage 150.

Executive Officers of the Registrant (at February 26, 2019):

 Age	Officer since
Virginia M. Rometty, Chairman of the Board, President and Chief Executive Officer*	61	2005
Michelle H. Browdy, Senior Vice President, Legal and Regulatory Affairs, and General Counsel	54	20
```

**Generated answer:**

IBM's main business segments are:

1. Cognitive Solutions
2. Global Business Services
3. Technology Services & Cloud Platforms
4. Systems

According to the provided information, Cognitive Solutions is the segment that contributes the largest share of revenue.

### Question 2 -- Fiscal Year 2015

**Q:** What does IBM disclose about its research and development spending and its strategic focus areas?

**Top retrieved chunk (truncated to 600 chars):**

```
Paired
with Watson is the company's core big data and analytics business. IBM has invested over $15 billion in these areas since 2010, including over $7 billion on more
than 20 acquisitions. Nearly half of IBM Research's spending is focused on analytics and cognitive.

 IBM's
leading-edge cognitive technology is only the starting point. The company is developing entirely new solutions businesses around that cognitive capability. In 2015, the Watson
Health unit was formed, which is IBM's first business unit designed around a single industry. Watson Health will create cognitive solutions that ca
```

**Generated answer:**

IBM annually invests approximately 6 percent of total revenue for R&D, focusing on high-growth, high-value opportunities. The company's strategic imperatives are centered around "digital" forces: big data and analytics, cloud and engagement.


---

## KMB

### Question 1 -- Fiscal Year 2018

**Q:** What are Kimberly-Clark's main product categories and which consumer brands does it own?

**Top retrieved chunk (truncated to 600 chars):**

```
KIMBERLY-CLARK CORPORATION -2018 Annual Report

 PART I

 ITEM 1. BUSINESS
 Kimberly-Clark Corporation was incorporated in Delaware in 1928. We are a global company focused on leading the world in essentials for a better life through product innovation and building our personal care, consumer tissue and K-C Professional brands. We are principally engaged in the manufacturing and marketing of a wide range of products mostly made from natural or synthetic fibers using advanced technologies in fibers, nonwovens and absorbency. Unless the context indicates otherwise, the terms "Corporation," "Kimb
```

**Generated answer:**

Kimberly-Clark's main product categories are Personal Care, Consumer Tissue, and K-C Professional. The company owns several well-known consumer brands, including:

* Personal Care: Huggies, Pull-Ups, Little Swimmers, GoodNites, DryNites, Kotex, U by Kotex, Intimus, Depend, Plenitud, Poise
* Consumer Tissue: Kleenex, Scott, Cottonelle, Viva, Andrex, Scottex, Neve
* K-C Professional: commercial tissue and wipers, skin care, safety and do-it-yourself products

### Question 2 -- Fiscal Year 2015

**Q:** How does Kimberly-Clark describe the impact of raw material costs (e.g. pulp) on its margins?

**Top retrieved chunk (truncated to 600 chars):**

```
4	KIMBERLY-CLARK CORPORATION- 2015 Annual Report

 adversely affected. In addition, the emergence of new sales channels may affect customer preferences and market dynamics and could adversely impact our financial results. These new channels include sales of consumer and other products via e-commerce, as well as the growth of large-format retailers and discounters that exclusively sell private-label products.
 Significant increases in prices for raw materials, energy, transportation and other necessary supplies and services, without corresponding increases in our selling prices, could adversely
```

**Generated answer:**

According to the context, Kimberly-Clark describes the impact of raw material costs, including pulp, as a potential adverse effect on its financial results if selling prices for finished products are not adjusted or if these adjustments significantly trail the increases in pulp prices. The company has not used derivative instruments to manage these risks.


---

## KR

### Question 1 -- Fiscal Year 2018

**Q:** How many stores does Kroger operate and what banners or formats does it use?

**Top retrieved chunk (truncated to 600 chars):**

```
Multi-department stores are significantly larger in size than combo stores. In addition to the departments offered at a typical combo store, multi-department stores sell a wide selection of general merchandise items such as apparel, home fashion and furnishings, outdoor living, electronics, automotive products, toys and fine jewelry.

 Marketplace stores are smaller in size than multi-department stores. They offer full-service grocery, pharmacy and health and beauty care departments as well as an expanded perishable offering and general merchandise area that includes apparel, home goods and to
```

**Generated answer:**

As of February 3, 2018, Kroger operates 2,782 supermarkets under various local banner names. The store formats used by Kroger include:

1. Combination food and drug stores ("combo stores")
2. Multi-department stores
3. Marketplace stores
4. Price impact warehouse stores

### Question 2 -- Fiscal Year 2015

**Q:** What does Kroger disclose about competition in the grocery retail industry?

**Top retrieved chunk (truncated to 600 chars):**

```
(2) Vitacost.com, Inc. (Vitacost.com) is included in our ending Consolidated Balance Sheets and Consolidated Statements of Operations for 2014.

 ITEM 7. MANAGEMENTS DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS.

 The following discussion and analysis of financial condition and results of operations of The Kroger Co. should be read in conjunction with the Forward-looking Statements section set forth in Part I, the Risk Factors section set forth in Item 1A of Part I and Outlook below.

 OUR BUSINESS

 The Kroger Co. was founded in 1883 and incorporated in 19
```

**Generated answer:**

Kroger discloses that the operating environment for the food retailing industry is characterized by intense price competition, aggressive expansion, increasing fragmentation of retail and online formats, entry of non-traditional competitors, and market consolidation.


---

## MS

### Question 1 -- Fiscal Year 2018

**Q:** What are Morgan Stanley's main business segments and the types of clients each serves?

**Top retrieved chunk (truncated to 600 chars):**

```
December 2018 Form 10-K	88	See Notes to Consolidated Financial Statements

 Notes to Consolidated Financial Statements

 1. Introduction and Basis of Presentation

 The Firm

 Morgan Stanley is a global financial services firm that maintains significant market positions in each of its business
segmentsInstitutional Securities, Wealth Management and Investment Management. Morgan Stanley, through its subsidiaries and affiliates, provides a wide variety of products and services to a large and diversified group of clients and customers,
including corporations, governments, financial institutions
```

**Generated answer:**

Morgan Stanley's main business segments are:

1. Institutional Securities: This segment provides investment banking, sales and trading, lending and other services to corporations, governments, financial institutions, and high to ultra-high net worth clients.
2. Wealth Management: This segment provides a comprehensive array of financial services and solutions to individual investors and small to medium-sized businesses and institutions, covering brokerage and investment advisory services, financial and wealth planning services, annuity and insurance products, securities-based lending, residential real estate loans, and other lending products.
3. Investment Management: This segment provides a broad range of investment strategies and products that span geographies, asset classes, and public and private markets to a diverse group of clients across institutional and intermediary channels.

Each segment serves different types of clients:

* Institutional Securities primarily serves corporations, governments, financial institutions, and high to ultra-high net worth clients.
* Wealth Management primarily serves individual investors and small to medium-sized businesses and institutions.
* Investment Management primarily serves institutional clients, including defined benefit/defined contribution plans, foundations, endowments, government entities, sovereign wealth funds, insurance companies, third-party fund sponsors, and corporations.

### Question 2 -- Fiscal Year 2015

**Q:** What does Morgan Stanley disclose about regulatory capital requirements and its capital ratios?

**Top retrieved chunk (truncated to 600 chars):**

```
(1)	Average balances were calculated based upon month-end balances.

 (2)	Tangible Morgan Stanley shareholders equity and tangible common equity are non-GAAP financial measures that the Company and investors consider
to be a useful measure to assess capital adequacy.

 Regulatory Requirements.

 Regulatory Capital Framework.

 The Company is a financial holding company under the Bank
Holding Company Act of 1956, as amended (the BHC Act), and is subject to the regulation and oversight of the Federal Reserve. The Federal Reserve establishes capital requirements for the Company, including well
```

**Generated answer:**

Morgan Stanley discloses that as of December 31, 2015, it had a Total risk-based capital ratio of at least 10%, a Tier 1 risk-based capital ratio of at least 8%, a Common Equity Tier 1 risk-based capital ratio of at least 6.5% and a Tier 1 leverage ratio of at least 5%.


---

## NVDA

### Question 1 -- Fiscal Year 2018

**Q:** What are NVIDIA's main product platforms and target markets?

**Top retrieved chunk (truncated to 600 chars):**

```
PART I

 ITEM 1. BUSINESS
 Our Company
 Starting with a focus on PC graphics, NVIDIA invented the graphics processing unit, or GPU, to solve some of the most complex problems in computer science. We have extended our focus in recent years to the revolutionary field of artificial intelligence, or AI. Fueled by the sustained demand for better 3D graphics and the scale of the gaming market, NVIDIA has evolved the GPU into a computer brain at the intersection of virtual reality, or VR, high performance computing, or HPC, and AI.
 The GPU was initially used to simulate human imagination, enabling t
```

**Generated answer:**

NVIDIA's two reportable segments - GPU and Tegra Processor - are based on a single underlying architecture. The main product platforms and target markets include:

1. Gaming:
   - GeForce for PC gaming and mainstream PCs
   - GeForce NOW for cloud-based game-streaming service
2. Professional Visualization:
   - Quadro for design professionals working in computer-aided design, video editing, special effects, and other creative applications
3. Datacenter:
   - Tesla for AI utilizing deep learning and accelerated computing, leveraging the parallel computing capabilities of GPUs for general purpose computing
   - NVIDIA GRID to provide the power of NVIDIA graphics through the cloud and datacenters
   - DGX for AI scientists, researchers and developers
4. Automotive:
   - DRIVEautomotive supercomputers and software stacks that provide self-driving capabilities
   - SHIELDdevices and services designed to harness the power of mobile-cloud to revolutionize home entertainment, AI and gaming
   - Jetson TX 2is a power-efficient AI computing platform for embedded use

### Question 2 -- Fiscal Year 2015

**Q:** What does NVIDIA say about competition in the GPU and data-center markets?

**Top retrieved chunk (truncated to 600 chars):**

```
(D)	On December 2, 2013, we issued$1.5 billionaggregate principal amount of1.00%Convertible Senior Notes due 2018.

 (E)	On June 10, 2011, we completed the acquisition of Icera, Inc. for total cash consideration of $352.2 million, and recorded goodwill of $271.2 million.

 ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS

 The following discussion and analysis of our financial condition and results of operations should be read in conjunction with “Item 1A. Risk Factors”, “Item 6. Selected Financial Data”, our Consolidated Financial Statements and re
```

**Generated answer:**

NVIDIA believes that the principal competitive factors in this market are performance, breadth of product offerings, access to customers and distribution channels, software support, conformity to industry standard Application Programming Interfaces, manufacturing capabilities, processor pricing and total system costs.


---

## PNC

### Question 1 -- Fiscal Year 2018

**Q:** What are PNC's main banking business segments and the types of products each offers?

**Top retrieved chunk (truncated to 600 chars):**

```
Corporate & Institutional Banking expanded its Corporate Banking business, focused on the middle market and larger sectors, into the Denver, Houston and Nashville markets in 2018. This followed offices opened in 2017 in Dallas, Kansas City and Minneapolis. These locations complement Corporate & Institutional Banking national businesses with a significant presence in these cities, and build on past successes in the markets where PNC’s retail banking presence was limited, such as in the Southeast. Our full suite of commercial products and services is offered in these locations. We have announced
```

**Generated answer:**

PNC's main banking business segments are Retail Banking and Corporate & Institutional Banking. 

Retail Banking provides demand deposit, money market and savings account products for consumer and small business customers, as well as debit card and net credit card fees.

Corporate & Institutional Banking offers a full suite of commercial products and services, including treasury management, capital markets-related products and services, and commercial mortgage banking activities.

### Question 2 -- Fiscal Year 2015

**Q:** What does PNC disclose about credit risk and its allowance for loan and lease losses?

**Top retrieved chunk (truncated to 600 chars):**

```
218The PNC Financial Services Group, Inc. Form 10-K

 SUMMARY OF LOAN LOSS EXPERIENCE

 Year ended December 31  dollars in millions	2015	2014	2013	2012	2011
Allowance for loan and lease losses  January 1	$	3,331	$	3,609	$	4,036	$	4,347	$	4,887
Charge-offs
Commercial	(206	)	(276	)	(395	)	(474	)	(700	)
Commercial real estate	(44	)	(70	)	(203	)	(314	)	(464	)
Equipment lease financing	(5	)	(14	)	(8	)	(16	)	(35	)
Home equity	(181	)	(275	)	(486	)	(560	)	(484	)
Residential real estate	(24	)	(40	)	(133	)	(110	)	(153	)
Credit card	(160	)	(163	)	(178	)	(200	)	(235	)
Other consumer	(185	)	(183	)	(185
```

**Generated answer:**

PNC discloses that it has policies, procedures, and practices to promote sound lending standards and prudent credit risk management. The company evaluates non-consolidated VIEs for consolidation based on accounting policies described in Note 1 Accounting Policies.

For commercial loans, PNC charges off nonperforming loans when a specific loan or portion thereof is uncollectible, considering factors such as the viability of the business or project, past due status, expected cash flows, collateral value, and guarantor willingness to perform.

The allowance for loan and lease losses is recorded at a level deemed appropriate to absorb estimated probable credit losses. The company determines the allowance based on periodic evaluations of unfunded credit facilities, including assessments of probability of commitment usage, credit risk factors, and terms and expiration dates of the facilities.

PNC also discloses that it has consolidated certain VIEs, such as Credit Card Securitization Trusts, where it is deemed the primary beneficiary due to its level of continuing involvement. The company consolidates these entities because PNC holds a variable interest in them and has the power to direct activities that most significantly affect their economic performance.

For residential mortgages and home equity loans/lines, PNC reports delinquent loans as 90 days or more past due or in process of foreclosure. Net charge-offs for these categories represent credit losses less recoveries distributed during the period.

The allowance for loan and lease losses is presented as a percentage of total loans, with the ratio varying by portfolio segment (59% for residential mortgages and 41% for consumer loans).


---

## PSA

### Question 1 -- Fiscal Year 2018

**Q:** Where are Public Storage's properties located and how many facilities does it operate?

**Top retrieved chunk (truncated to 600 chars):**

```
At December 31, 201 8 , 30 of our U.S. facilities with a net book value of $1 1 1 million were encumbered by an aggregate of $ 2 7 million in mortgage notes payable.

 We have no specific policy as to the maximum size of any one particular self-storage facility. However, none of our facilities involves, or is expected to involve, 1% or more of our total assets, gross revenues or net income.

 Description of Self-Storage Facilities: Self-storage facilities, which comprise the majority of our investments, offer accessible storage space for personal and business use at a relatively low cost. A us
```

**Generated answer:**

Public Storage operates self-storage facilities primarily in or near major metropolitan markets in 38 states in the U.S. It also has facilities in Europe under the "Shurgard" brand name.

The company manages 30 U.S. facilities with a net book value of $111 million that were encumbered by an aggregate of $27 million in mortgage notes payable as of December 31, 2018.

### Question 2 -- Fiscal Year 2015

**Q:** What does Public Storage disclose about its primary sources of revenue and occupancy rates?

**Top retrieved chunk (truncated to 600 chars):**

```
On our website, www.publicstorage.com , we make available, free of charge, our Annual Reports on Form 10-K, quarterly reports on Form 10-Q, current reports on Form 8-K, and all amendments to those reports as soon as reasonably practicable after the reports and amendments are electronically filed with or furnished to the SEC.

 Competition

 We believe that storage customers generally store their goods within a five mile radius of their home or business . Our facilities compete with nearby self-storage facilities owned by other operators using marketing channels similar to ours , including Inte
```

**Generated answer:**

Public Storage discloses that its primary source of revenue is from self-storage facilities, with revenues of $2,235,525 for the year ended December 31, 2015. It also mentions that it generates ancillary revenues from merchandise sales and tenant reinsurance. The company reports that occupancy levels are generally higher in the summer months than in the winter months, but does not provide specific occupancy rates.


---

## TECH

### Question 1 -- Fiscal Year 2018

**Q:** What products does Bio-Techne (TECH) sell and which scientific markets does it serve?

**Top retrieved chunk (truncated to 600 chars):**

```
Recognizing the importance of an integrated, global approach to meeting our mission and accomplishing our strategies, we have over the past several years unified our brands and recent acquisitions under a single global brand, Bio-Techne.

 We are committed to providing the life sciences community with innovative, high-quality scientific tools that allow our customers to make extraordinary discoveries. Our mission is to build “epic tools for epic science.” We intend to build on Bio-Techne’s past accomplishments, high product quality reputation and sound financial position by executing strategie
```

**Generated answer:**

Bio-Techne (TECH) sells specialized proteins, including cytokines and growth factors, immunoassays, antibodies, and related reagents to the biotechnology research community. It serves two primary scientific markets:

1. Biotechnology: Bio-Techne provides consumables used for conducting laboratory experiments by both industry and academic scientists within the biotechnology and biomedical life sciences fields.
2. Diagnostics: Bio-Techne provides a range of controls and calibrators used with diagnostic equipment and as proficiency testing tools, as well as other reagents incorporated into diagnostic kits.

These products are sold directly to customers primarily located in North America, Europe, and China, with sales distributed widely across various end-users.

### Question 2 -- Fiscal Year 2015

**Q:** What does the company disclose about its acquisition strategy and recent acquisitions?

**Top retrieved chunk (truncated to 600 chars):**

```
External sales are attributed to countries based on the location of the customer or distributor. Long-lived assets are comprised of land, buildings and improvements and equipment, net of accumulated depreciation and other assets.

 Note 13. Supplemental Disclosures of Cash Flow Information and Noncash Investing and Financing Activities:

 In fiscal 2015, the Company acquired Novus, ProteinSimple, and CyVek for approximately $60 million, $300 million and $95 million, respectively. CyVek was acquired for approximately $62 million in cash and the Company will also pay CyVek’s previous stockholder
```

**Generated answer:**

The Company discloses that it is pursuing new lease space for its Tocris operations. The Company also acquired Cliniqa Corporation on July 8, 2015, expanding and complementing its clinical controls product lines.


---

_Evaluation completed in 1520.2s._
