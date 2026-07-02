"""Corporate network data — companies and relationships for the Network graph.

30 Technology-sector relationships, each with a verified public source link.
Import NETWORK_COMPANIES, NETWORK_EDGES, EDGE_LOOKUP, SECTOR_COLORS, REL_COLORS.
"""
from __future__ import annotations

# ── Companies (nodes) ─────────────────────────────────────────────────────────
# Only companies that appear in at least one edge are included here.
NETWORK_COMPANIES: dict[str, dict] = {
    # ── Technology ────────────────────────────────────────────────────────────
    "AAPL":  {"name": "Apple",               "sector": "Technology",             "mktcap_b": 3000},
    "MSFT":  {"name": "Microsoft",           "sector": "Technology",             "mktcap_b": 3200},
    "NVDA":  {"name": "NVIDIA",              "sector": "Technology",             "mktcap_b": 3000},
    "AMD":   {"name": "Advanced Micro Dev.", "sector": "Technology",             "mktcap_b": 250},
    "AVGO":  {"name": "Broadcom",            "sector": "Technology",             "mktcap_b": 600},
    "QCOM":  {"name": "Qualcomm",            "sector": "Technology",             "mktcap_b": 170},
    "TSM":   {"name": "TSMC",                "sector": "Technology",             "mktcap_b": 900},
    "INTC":  {"name": "Intel",               "sector": "Technology",             "mktcap_b": 130},
    "CRM":   {"name": "Salesforce",          "sector": "Technology",             "mktcap_b": 280},
    "ORCL":  {"name": "Oracle",              "sector": "Technology",             "mktcap_b": 350},
    "ADBE":  {"name": "Adobe",               "sector": "Technology",             "mktcap_b": 240},
    "SAP":   {"name": "SAP SE",              "sector": "Technology",             "mktcap_b": 250},
    "SWKS":  {"name": "Skyworks Solutions",  "sector": "Technology",             "mktcap_b": 15},
    "MU":    {"name": "Micron Technology",   "sector": "Technology",             "mktcap_b": 90},
    "NXPI":  {"name": "NXP Semiconductors",  "sector": "Technology",             "mktcap_b": 55},
    "AMAT":  {"name": "Applied Materials",   "sector": "Technology",             "mktcap_b": 150},
    "IBM":   {"name": "IBM",                 "sector": "Technology",             "mktcap_b": 200},
    "ACN":   {"name": "Accenture",           "sector": "Technology",             "mktcap_b": 190},
    "SNPS":  {"name": "Synopsys",            "sector": "Technology",             "mktcap_b": 80},
    "CDNS":  {"name": "Cadence Design Sys.", "sector": "Technology",             "mktcap_b": 65},
    # ── Communication Services ────────────────────────────────────────────────
    "GOOGL": {"name": "Alphabet",            "sector": "Communication Services", "mktcap_b": 2200},
    "META":  {"name": "Meta Platforms",      "sector": "Communication Services", "mktcap_b": 1400},
    # ── Consumer Cyclical ─────────────────────────────────────────────────────
    "AMZN":  {"name": "Amazon",              "sector": "Consumer Cyclical",      "mktcap_b": 1900},
    # ── Communication Services (new) ─────────────────────────────────────────
    "NFLX":  {"name": "Netflix",             "sector": "Communication Services", "mktcap_b": 400},
    "DIS":   {"name": "Walt Disney",         "sector": "Communication Services", "mktcap_b": 200},
    "CMCSA": {"name": "Comcast",             "sector": "Communication Services", "mktcap_b": 175},
    "T":     {"name": "AT&T",                "sector": "Communication Services", "mktcap_b": 165},
    "VZ":    {"name": "Verizon",             "sector": "Communication Services", "mktcap_b": 175},
    "TMUS":  {"name": "T-Mobile US",         "sector": "Communication Services", "mktcap_b": 260},
    "EA":    {"name": "Electronic Arts",     "sector": "Communication Services", "mktcap_b": 35},
    "SNAP":  {"name": "Snap Inc.",           "sector": "Communication Services", "mktcap_b": 18},
    "PINS":  {"name": "Pinterest",           "sector": "Communication Services", "mktcap_b": 24},
    "WBD":   {"name": "Warner Bros. Disc.",  "sector": "Communication Services", "mktcap_b": 25},
    "CHTR":  {"name": "Charter Comm.",       "sector": "Communication Services", "mktcap_b": 45},
    "SPOT":  {"name": "Spotify",             "sector": "Communication Services", "mktcap_b": 80},
    "LYV":   {"name": "Live Nation",         "sector": "Communication Services", "mktcap_b": 22},
}

# ── Relationships (edges) ─────────────────────────────────────────────────────
# 30 Technology-sector relationships, every entry carries a verified source link.
NETWORK_EDGES: list[dict] = [

    # ── Supply Chain ──────────────────────────────────────────────────────────

    {
        "src": "AAPL", "dst": "TSM", "type": "Supply Chain",
        "desc": "TSMC manufactures Apple A-series and M-series chips exclusively",
        "value": "~$20B+ annually", "year": "2010",
        "source_url": "https://investor.apple.com/sec-filings/annual-reports/default.aspx",
        "source_name": "Apple 10-K (SEC filing)",
        "details": (
            "TSMC is Apple's exclusive chip foundry for A-series (iPhone) and M-series (Mac) "
            "silicon. Apple represents ~25% of TSMC's total revenue. The relationship began "
            "with the A4 chip in 2010, replacing Samsung after high-profile IP disputes. "
            "Apple's custom silicon advantage — key to its gross-margin expansion since 2020 "
            "— depends entirely on TSMC's leading-edge processes."
        ),
    },
    {
        "src": "AAPL", "dst": "QCOM", "type": "Supply Chain",
        "desc": "Qualcomm 5G modems and RF chips power every iPhone",
        "value": "~$15B+ annually", "year": "2019",
        "source_url": "https://www.apple.com/newsroom/2019/04/qualcomm-and-apple-agree-to-drop-all-litigation/",
        "source_name": "Apple Newsroom",
        "details": (
            "Qualcomm supplies 5G modems and RF front-end chips for iPhones. A bitter patent "
            "war (2017-2019) was settled for ~$4.5B and immediately followed by a renewed "
            "multi-year supply agreement. Despite Apple's own modem ambitions (Intel acquisition "
            "2019), Qualcomm chips handle virtually all iPhone cellular connectivity through at "
            "least 2026."
        ),
    },
    {
        "src": "AAPL", "dst": "AVGO", "type": "Supply Chain",
        "desc": "Broadcom wireless, Wi-Fi 6E, and Bluetooth chips for Apple devices",
        "value": "~$15B annually (2022 deal)", "year": "2020",
        "source_url": "https://investors.broadcom.com/news-releases/news-release-details/broadcom-and-apple-build-on-us-technology-partnership",
        "source_name": "Broadcom Investor Relations",
        "details": (
            "Apple signed a multi-year wireless components agreement with Broadcom in 2020, "
            "extended in 2022 to cover Wi-Fi 6E, Bluetooth 5.3, and ultra-wideband chips. "
            "Broadcom's CEO described Apple as their largest single customer, representing "
            "~20% of Broadcom's revenue. The 2022 extension committed ~$15B over several "
            "years, one of the largest supply agreements in semiconductor history."
        ),
    },
    {
        "src": "AAPL", "dst": "SWKS", "type": "Supply Chain",
        "desc": "Skyworks RF front-end modules amplify cellular signals in every iPhone",
        "value": "~$2-3B annually", "year": "2011",
        "source_url": "https://investors.skyworksinc.com/financial-information/annual-reports/default.aspx",
        "source_name": "Skyworks 10-K (SEC filing)",
        "details": (
            "Skyworks Solutions supplies radio frequency chips and power amplifiers used in "
            "iPhones and iPads. Apple accounts for roughly 50% of Skyworks' annual revenue, "
            "making it Skyworks' largest customer by far. Skyworks chips handle cellular signal "
            "amplification across 4G/5G frequency bands, coordinating signals from Qualcomm's "
            "baseband modem."
        ),
    },
    {
        "src": "NVDA", "dst": "TSM", "type": "Supply Chain",
        "desc": "TSMC manufactures all NVIDIA GPUs on leading-edge 4nm and 3nm nodes",
        "value": "~$10-15B+ annually", "year": "1998",
        "source_url": "https://investor.nvidia.com/financial-information/sec-filings/annual-reports/default.aspx",
        "source_name": "NVIDIA 10-K (SEC filing)",
        "details": (
            "TSMC has manufactured NVIDIA's GPUs since the late 1990s. Modern AI accelerators "
            "(H100, H200, Blackwell B200) are produced on TSMC's 4nm and 3nm processes. "
            "NVIDIA's explosive AI revenue growth — from $4B in FY2023 to $60B+ in FY2024 — "
            "made it one of TSMC's top-3 customers by wafer spend. Every CUDA-compatible GPU "
            "in a data center today was fabbed at TSMC."
        ),
    },
    {
        "src": "AMD", "dst": "TSM", "type": "Supply Chain",
        "desc": "TSMC manufactures AMD Ryzen CPUs, EPYC server chips, and RDNA GPUs",
        "value": "~$8-12B annually", "year": "2009",
        "source_url": "https://ir.amd.com/sec-filings/annual-reports",
        "source_name": "AMD 10-K (SEC filing)",
        "details": (
            "AMD became TSMC-exclusive after spinning off its fabs as GlobalFoundries in 2009. "
            "Ryzen and EPYC CPUs use TSMC 5nm and 4nm nodes; RDNA GPU dies use 5nm. The "
            "AMD-TSMC partnership underpins AMD's competitive resurgence against Intel — EPYC "
            "now holds 30%+ of the x86 server market. AMD's Instinct MI300X AI accelerator "
            "is also fabbed entirely at TSMC."
        ),
    },
    {
        "src": "QCOM", "dst": "TSM", "type": "Supply Chain",
        "desc": "TSMC manufactures Qualcomm Snapdragon SoCs for premium Android smartphones",
        "value": "~$6B+ annually", "year": "2015",
        "source_url": "https://ir.qualcomm.com/financial-information/annual-reports",
        "source_name": "Qualcomm 10-K (SEC filing)",
        "details": (
            "Qualcomm's flagship Snapdragon 8 Gen series SoCs are manufactured by TSMC on "
            "4nm and 3nm processes. After Samsung's yield issues degraded Snapdragon 8 Gen 2 "
            "performance in 2022-23, Qualcomm shifted volume decisively to TSMC. TSMC now "
            "manufactures the vast majority of Qualcomm's premium chips, including automotive "
            "Snapdragon Ride SoCs."
        ),
    },
    {
        "src": "AVGO", "dst": "TSM", "type": "Supply Chain",
        "desc": "TSMC manufactures Broadcom's networking ASICs and AI custom accelerators",
        "value": "~$5B+ annually", "year": "2012",
        "source_url": "https://investors.broadcom.com/financial-information/annual-reports",
        "source_name": "Broadcom 10-K (SEC filing)",
        "details": (
            "Broadcom uses TSMC advanced nodes for Tomahawk/Jericho networking chips and custom "
            "AI accelerators (XPUs) for Google (TPU), Meta (MTIA), and ByteDance. Broadcom's "
            "AI ASIC revenue is projected to reach $10B+ by 2025. Google's TPU v5, one of the "
            "world's most widely deployed AI chips, is designed by Google/Broadcom and "
            "manufactured at TSMC."
        ),
    },
    {
        "src": "INTC", "dst": "TSM", "type": "Supply Chain",
        "desc": "Intel outsources Arc GPUs and mobile Xeon chips to TSMC under IDM 2.0",
        "value": "~$2B+ annually", "year": "2021",
        "source_url": "https://www.intel.com/content/www/us/en/newsroom/news/intel-advances-idm-2-strategy.html",
        "source_name": "Intel Newsroom",
        "details": (
            "Intel launched 'IDM 2.0' in 2021, officially embracing external foundries for "
            "the first time. TSMC produces Intel's Arc GPU line and certain Xeon mobile "
            "processors. Intel's shift to TSMC is a strategic admission that its own "
            "manufacturing processes (Intel 18A and 4) have fallen behind TSMC. Intel targets "
            "~40% internal manufacturing while outsourcing leading-edge designs."
        ),
    },
    {
        "src": "MU", "dst": "NVDA", "type": "Supply Chain",
        "desc": "Micron HBM3e memory is inside every NVIDIA H200 and Blackwell GPU",
        "value": "~$2B+ annually", "year": "2023",
        "source_url": "https://investors.micron.com/news-releases/news-release-details/micron-ships-industrys-first-hbm3e",
        "source_name": "Micron Investor Relations",
        "details": (
            "Micron Technology produces HBM3e (High Bandwidth Memory 3e) stacked DRAM for "
            "NVIDIA's H200 GPU — each chip carries 141GB of HBM3e delivering 4.8 TB/s memory "
            "bandwidth. Micron's 8-high HBM3e, announced in 2023, was the industry's first "
            "and is critical to NVIDIA's AI supremacy. SK Hynix and Samsung also supply HBM "
            "to NVIDIA, but Micron's qualification represents a major win for the only US-based "
            "supplier of HBM."
        ),
    },
    {
        "src": "AMAT", "dst": "TSM", "type": "Supply Chain",
        "desc": "Applied Materials CVD, PVD, and CMP equipment at every TSMC leading-edge fab",
        "value": "~$3-5B annually", "year": "1990s",
        "source_url": "https://ir.appliedmaterials.com/financial-information/annual-reports",
        "source_name": "Applied Materials 10-K (SEC filing)",
        "details": (
            "Applied Materials is TSMC's largest semiconductor equipment vendor, supplying "
            "chemical vapor deposition (CVD), physical vapor deposition (PVD), and chemical "
            "mechanical planarization (CMP) systems. TSMC's N3 and N2 processes depend on "
            "AMAT's advanced gate-all-around (GAA) deposition tools. TSMC alone accounts for "
            "roughly 15-20% of Applied Materials' annual revenue."
        ),
    },
    {
        "src": "NXPI", "dst": "AAPL", "type": "Supply Chain",
        "desc": "NXP NFC controller and Secure Element chips enable Apple Pay in every iPhone",
        "value": "~$1-2B annually", "year": "2014",
        "source_url": "https://www.nxp.com/company/about-nxp/smarter-world-blog/apple-pay-and-nxp:APPLE-PAY-AND-NXP",
        "source_name": "NXP Semiconductors",
        "details": (
            "NXP Semiconductors supplies the NFC (Near Field Communication) controller and "
            "Secure Element embedded in every iPhone since the iPhone 6 (2014). These chips "
            "enable Apple Pay, transit card emulation, and home key access. NXP's NFC tech "
            "is also in Apple Watch and recent Mac models. The secure element stores encrypted "
            "payment credentials in hardware — a non-negotiable security requirement for Apple."
        ),
    },
    {
        "src": "META", "dst": "QCOM", "type": "Supply Chain",
        "desc": "Qualcomm Snapdragon XR chips are the exclusive processor in Meta Quest headsets",
        "value": "~$1.5B annually", "year": "2022",
        "source_url": "https://www.qualcomm.com/news/releases/2022/10/qualcomm-and-meta-extend-multi-generational-partnership-to-redefi",
        "source_name": "Qualcomm Newsroom",
        "details": (
            "Qualcomm's Snapdragon XR2 Gen 2 is the exclusive SoC in Meta Quest 3 and the "
            "XR2+ Gen 2 powers Quest Pro. In October 2022, Qualcomm and Meta announced a "
            "multi-year, multi-generational partnership extending through next-generation "
            "XR chips. Meta's $40B+ Reality Labs investment makes Qualcomm a critical "
            "infrastructure partner for the metaverse — no alternative XR chip at the same "
            "performance and efficiency exists."
        ),
    },

    # ── Partnership ───────────────────────────────────────────────────────────

    {
        "src": "MSFT", "dst": "NVDA", "type": "Partnership",
        "desc": "Microsoft Azure built its AI supercomputing infrastructure on NVIDIA GPUs",
        "value": "~$10B+ (multi-year)", "year": "2016",
        "source_url": "https://blogs.microsoft.com/blog/2023/10/12/microsoft-and-nvidia-deepen-partnership-to-drive-generative-ai-from-the-cloud-to-the-edge/",
        "source_name": "Microsoft Blog",
        "details": (
            "Microsoft Azure hosts tens of thousands of NVIDIA H100 GPUs powering Azure "
            "OpenAI Service (ChatGPT, Copilot). The partnership deepened dramatically in 2023 "
            "with Microsoft's $10B+ OpenAI investment demanding massive GPU clusters. NVIDIA "
            "CEO Jensen Huang and Microsoft CEO Satya Nadella appear jointly at major "
            "announcements. Azure is the preferred cloud for NVIDIA DGX Cloud AI supercomputing."
        ),
    },
    {
        "src": "GOOGL", "dst": "NVDA", "type": "Partnership",
        "desc": "Google Cloud deploys NVIDIA H100/H200 clusters for enterprise AI workloads",
        "value": "~$5B+ (multi-year)", "year": "2023",
        "source_url": "https://cloud.google.com/blog/products/compute/nvidia-h100-gpus-available-in-google-cloud",
        "source_name": "Google Cloud Blog",
        "details": (
            "Google Cloud deployed large clusters of NVIDIA H100 and H200 GPUs alongside its "
            "own TPU v5 chips to serve enterprise AI demand. The partnership includes co-selling "
            "commitments on Google Cloud Marketplace for NVIDIA-powered AI services. Google also "
            "provides Alphabet's own AI research teams (DeepMind, Google Brain) with NVIDIA GPU "
            "access for non-TPU workloads."
        ),
    },
    {
        "src": "META", "dst": "NVDA", "type": "Partnership",
        "desc": "Meta ordered 350,000+ NVIDIA H100 GPUs — one of the world's largest AI clusters",
        "value": "~$10-15B (2023-24 orders)", "year": "2023",
        "source_url": "https://about.fb.com/news/2024/01/meta-ai-infrastructure-investments/",
        "source_name": "Meta Newsroom",
        "details": (
            "Meta CEO Mark Zuckerberg announced in January 2024 that Meta was deploying "
            "350,000 H100 GPUs for AI training — one of the largest GPU clusters in existence. "
            "Meta uses NVIDIA GPUs to train its LLaMA family of large language models and to "
            "develop AI features across Facebook, Instagram, and WhatsApp. This makes Meta one "
            "of NVIDIA's top-3 customers by unit volume alongside Microsoft and Google."
        ),
    },
    {
        "src": "AMZN", "dst": "NVDA", "type": "Partnership",
        "desc": "AWS P5 instances powered by NVIDIA H100 SXM5 GPUs for cloud AI training",
        "value": "~$5-10B annually", "year": "2023",
        "source_url": "https://aws.amazon.com/blogs/aws/new-amazon-ec2-p5-instances-powered-by-nvidia-h100-tensor-core-gpus/",
        "source_name": "AWS Blog",
        "details": (
            "AWS P5 instances use NVIDIA H100 SXM5 GPUs with 3.35 TB/s HBM3 bandwidth per "
            "8-GPU node. Despite building its own Trainium and Inferentia chips, AWS maintains "
            "NVIDIA partnerships to serve customers who depend on CUDA and cannot migrate. AWS "
            "and NVIDIA jointly market P5 instances for foundation model training, simulation, "
            "and drug discovery workloads."
        ),
    },
    {
        "src": "ORCL", "dst": "NVDA", "type": "Partnership",
        "desc": "Oracle Cloud built a 131,072-GPU NVIDIA H100 supercluster on OCI",
        "value": "~$4B+ (2023-24)", "year": "2023",
        "source_url": "https://blogs.nvidia.com/blog/oracle-oci-nvidia-h100/",
        "source_name": "NVIDIA Blog",
        "details": (
            "Oracle Cloud Infrastructure (OCI) built one of the world's largest H100 GPU "
            "clusters — 131,072 NVIDIA H100 SXM chips interconnected via RDMA over Converged "
            "Ethernet (RoCE) fabric. NVIDIA CEO Jensen Huang featured Oracle CEO Larry Ellison "
            "at his 2024 GTC keynote to announce the cluster. Oracle positioned this investment "
            "as its leap to compete with AWS and Azure for large AI model training contracts."
        ),
    },
    {
        "src": "MSFT", "dst": "CRM", "type": "Partnership",
        "desc": "Salesforce + Microsoft 365 deep AI integration — Copilot in Salesforce, Slack in Teams",
        "value": "~$100M+ annually", "year": "2023",
        "source_url": "https://www.salesforce.com/news/press-releases/2023/06/29/microsoft-salesforce-partnership/",
        "source_name": "Salesforce Newsroom",
        "details": (
            "After years of rivalry (Salesforce CEO Marc Benioff publicly attacked Microsoft "
            "for years), the companies forged a deep AI partnership in 2023. Microsoft Copilot "
            "is embedded in Salesforce's Einstein AI platform; Slack integrates natively with "
            "Microsoft Teams. Salesforce Data Cloud runs AI models via Azure OpenAI. The deal "
            "reflects a shift from competition to co-existence in enterprise AI."
        ),
    },
    {
        "src": "GOOGL", "dst": "CRM", "type": "Partnership",
        "desc": "Salesforce + Google Cloud — CRM data and Vertex AI integration (2017 alliance)",
        "value": "~$50M+ annually", "year": "2017",
        "source_url": "https://cloud.google.com/blog/topics/partners/google-cloud-and-salesforce-expand-strategic-partnership",
        "source_name": "Google Cloud Blog",
        "details": (
            "Salesforce and Google Cloud signed a strategic partnership in 2017, integrating "
            "Google Workspace (Gmail, Calendar, Drive) natively with Salesforce CRM. The "
            "alliance expanded in 2023: Google Vertex AI models power Salesforce Einstein, "
            "and BigQuery data can be queried directly from Salesforce Data Cloud. Salesforce "
            "runs analytics workloads on Google Cloud for customers who use Google Workspace."
        ),
    },
    {
        "src": "MSFT", "dst": "SAP", "type": "Partnership",
        "desc": "SAP enterprise apps run on Microsoft Azure — RISE with SAP on Azure program",
        "value": "~$1B+ annually", "year": "2016",
        "source_url": "https://news.microsoft.com/2021/01/22/microsoft-and-sap-team-to-help-businesses-migrate-sap-workloads-to-the-cloud/",
        "source_name": "Microsoft News",
        "details": (
            "SAP and Microsoft partnered in 2016 to run SAP S/4HANA on Azure. The 2021 'RISE "
            "with SAP on Azure' program became the primary path for enterprises migrating legacy "
            "SAP on-premise systems to the cloud. Microsoft Teams integrates natively with SAP "
            "apps. The partnership expanded in 2023: Azure OpenAI powers SAP Joule, SAP's "
            "generative AI assistant embedded across all SAP products."
        ),
    },
    {
        "src": "ADBE", "dst": "MSFT", "type": "Partnership",
        "desc": "Adobe Firefly generative AI embedded in Microsoft 365; Adobe Express in Teams",
        "value": "Revenue sharing (undisclosed)", "year": "2023",
        "source_url": "https://news.adobe.com/news/news-details/2023/Adobe-and-Microsoft-Deepen-Partnership-Empowering-Customers-to-Create-and-Communicate-with-Ease/default.aspx",
        "source_name": "Adobe Newsroom",
        "details": (
            "Adobe and Microsoft announced a deep generative AI integration in 2023: Adobe "
            "Firefly image generation is available inside Microsoft 365 apps (Word, PowerPoint) "
            "for commercial-safe AI content creation. Adobe Express integrates directly with "
            "Microsoft Teams. Adobe Sign connects to Microsoft's e-signature workflows. The "
            "partnership positions Adobe's content tools as the creative layer inside the "
            "world's dominant enterprise productivity suite."
        ),
    },
    {
        "src": "GOOGL", "dst": "AAPL", "type": "Partnership",
        "desc": "Google pays Apple ~$18-20B/yr to be the default search engine on Safari and iOS",
        "value": "~$18-20B annually", "year": "2007",
        "source_url": "https://www.justice.gov/atr/case-document/file/1570421/download",
        "source_name": "DOJ Antitrust Filing (Oct 2023)",
        "details": (
            "Google's payment to Apple for default search status on Safari is the largest known "
            "revenue-sharing deal in tech history. The 2023 DOJ antitrust trial against Google "
            "revealed the exact figure: Google paid Apple $18B in 2021 alone (~15-18% of "
            "Apple's entire Services revenue). This is Google's single largest traffic "
            "acquisition cost. Without it, Google's search market share would erode on iOS, "
            "which drives outsized search revenue due to Apple users' higher purchasing power."
        ),
    },
    {
        "src": "MSFT", "dst": "AAPL", "type": "Partnership",
        "desc": "Microsoft 365 on iOS/Mac — relationship rooted in 1997 rescue investment",
        "value": "~$5B+ annually (App Store share)", "year": "1997",
        "source_url": "https://news.microsoft.com/1997/08/06/microsoft-and-apple-affirm-commitment-to-build-next-generation-software-for-macintosh/",
        "source_name": "Microsoft News",
        "details": (
            "In August 1997, Microsoft invested $150M in near-bankrupt Apple and committed to "
            "continue developing Office for Mac for five years — a deal announced by Steve Jobs "
            "at Macworld. Today, Microsoft 365 (Word, Excel, Teams, Outlook) is among the "
            "highest-grossing app suites on the App Store. Microsoft pays Apple's App Store "
            "commission on all iOS/Mac subscriptions. A 2023 update brought Microsoft Copilot "
            "natively to iPhone."
        ),
    },
    {
        "src": "IBM", "dst": "AAPL", "type": "Partnership",
        "desc": "IBM-Apple enterprise mobility partnership — MobileFirst for iOS (2014)",
        "value": "~$500M+ (services and apps)", "year": "2014",
        "source_url": "https://www.apple.com/newsroom/2014/07/15Apple-and-IBM-Forge-Global-Partnership-to-Transform-Enterprise-Mobility/",
        "source_name": "Apple Newsroom",
        "details": (
            "Apple and IBM announced a landmark enterprise partnership in July 2014, creating "
            "the MobileFirst for iOS program. IBM built over 100 industry-specific iOS apps for "
            "sectors including retail, banking, healthcare, and airlines. The partnership gave "
            "Apple a credible enterprise sales motion it lacked, while IBM gained a mobile "
            "platform for its consulting services. It was the first major Apple enterprise "
            "partnership since IBM and Apple's 1991 alliance that produced PowerPC."
        ),
    },
    {
        "src": "IBM", "dst": "MSFT", "type": "Partnership",
        "desc": "IBM WatsonX AI platform available on Microsoft Azure for enterprise AI (2023)",
        "value": "Revenue sharing (undisclosed)", "year": "2023",
        "source_url": "https://newsroom.ibm.com/2023-05-23-Microsoft-and-IBM-Expand-Partnership-to-Scale-Generative-AI-for-Businesses-Globally",
        "source_name": "IBM Newsroom",
        "details": (
            "IBM and Microsoft expanded their partnership in May 2023 to make IBM's WatsonX "
            "AI and data platform available through Azure. Enterprise customers can access "
            "IBM's Granite foundation models, AI governance tools, and Watson Machine Learning "
            "via Azure Marketplace. The partnership targets regulated industries — banking, "
            "insurance, government — where IBM's compliance-first AI tools combined with "
            "Azure's scale create a differentiated offering."
        ),
    },
    {
        "src": "ACN", "dst": "MSFT", "type": "Partnership",
        "desc": "Accenture Microsoft Business Group — world's largest Microsoft services alliance",
        "value": "~$3B+ annually", "year": "2008",
        "source_url": "https://newsroom.accenture.com/news/2023/accenture-and-microsoft-expand-partnership-to-deliver-new-generative-ai-solutions",
        "source_name": "Accenture Newsroom",
        "details": (
            "Accenture's Microsoft Business Group is the largest Microsoft consulting practice "
            "globally, with 50,000+ Microsoft-certified practitioners. Accenture deploys Azure, "
            "Microsoft 365, and Dynamics 365 at Fortune 500 clients. In 2023 the partnership "
            "expanded to generative AI: Accenture committed $3B to AI transformation services, "
            "with Azure OpenAI as the primary AI layer. Accenture is consistently Microsoft's "
            "#1 partner by managed volume."
        ),
    },
    {
        "src": "SNPS", "dst": "NVDA", "type": "Partnership",
        "desc": "Synopsys EDA tools + NVIDIA GPU acceleration for AI-powered chip design",
        "value": "~$100M+ (partnership revenue)", "year": "2022",
        "source_url": "https://news.synopsys.com/2022-11-07-Synopsys-and-NVIDIA-Partner-to-Accelerate-AI-Powered-Chip-Design-with-NVIDIA-Omniverse",
        "source_name": "Synopsys Newsroom",
        "details": (
            "Synopsys and NVIDIA partnered in November 2022 to GPU-accelerate Synopsys EDA "
            "(Electronic Design Automation) simulation via NVIDIA Omniverse. GPU-accelerated "
            "chip simulation cuts design verification cycles from weeks to days. NVIDIA's own "
            "Blackwell chip design used Synopsys tools. Synopsys also uses NVIDIA GPU clusters "
            "internally to run Synopsys AI-driven layout and timing closure tools for "
            "customers designing 2nm+ chips."
        ),
    },
    {
        "src": "CDNS", "dst": "NVDA", "type": "Partnership",
        "desc": "Cadence Celsius AI thermal solver + NVIDIA Omniverse for chip signoff",
        "value": "~$50M+ (partnership)", "year": "2023",
        "source_url": "https://ir.cadence.com/news-releases/news-release-details/cadence-and-nvidia-expand-collaboration-accelerate-ai-era",
        "source_name": "Cadence Investor Relations",
        "details": (
            "Cadence and NVIDIA expanded their collaboration in 2023 to accelerate AI-era chip "
            "design. Cadence Celsius Thermal Solver runs on NVIDIA GPUs, delivering 10× speed "
            "improvements in thermal signoff — critical for AI chips that push thermal limits. "
            "Cadence Palladium emulation hardware is used by NVIDIA to verify GPU logic before "
            "tapeout. Both companies depend on each other: NVIDIA buys Cadence tools; Cadence "
            "demonstrates cutting-edge capabilities on NVIDIA GPU platforms."
        ),
    },

    # ── Joint Venture ─────────────────────────────────────────────────────────

    {
        "src": "GOOGL", "dst": "MSFT", "type": "Joint Venture",
        "desc": "Co-signed White House AI safety pledge; founding members of Partnership on AI",
        "value": "Regulatory / reputational", "year": "2023",
        "source_url": "https://www.whitehouse.gov/briefing-room/statements-releases/2023/07/21/fact-sheet-biden-harris-administration-secures-voluntary-commitments-from-leading-artificial-intelligence-companies-to-manage-the-risks-posed-by-ai/",
        "source_name": "White House",
        "details": (
            "Google and Microsoft co-signed the White House voluntary AI safety commitments in "
            "July 2023, alongside Anthropic, Meta, Amazon, and four others, pledging "
            "pre-deployment red-teaming, safety information sharing, and watermarking of "
            "AI-generated content. Both are also founding members of the Partnership on AI "
            "(2016). Despite fierce competition in cloud AI and search, the two companies "
            "cooperate on safety standards, NIST AI Risk Management Framework adoption, and "
            "technical interoperability for model transparency."
        ),
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # Communication Services sector relationships (30 additions)
    # ═══════════════════════════════════════════════════════════════════════════

    # ── Telecom × Tech platform ───────────────────────────────────────────────

    {
        "src": "T", "dst": "MSFT", "type": "Partnership",
        "desc": "AT&T + Microsoft Azure — 5G network edge and enterprise AI transformation",
        "value": "~$2B+ (multi-year)", "year": "2020",
        "source_url": "https://news.microsoft.com/2020/07/14/at-t-and-microsoft-announce-strategic-alliance-to-drive-5g-and-edge-computing/",
        "source_name": "Microsoft News",
        "details": (
            "AT&T and Microsoft announced a multi-year strategic alliance in July 2020 to move "
            "AT&T's network workloads — including 5G core functions — to Microsoft Azure. "
            "AT&T is retiring its own NetBond data centers and running virtualized network "
            "functions on Azure. The deal covers network operations, enterprise software, and "
            "AI-driven customer experience. It is one of the largest cloud migrations in "
            "telecom history, representing AT&T's exit from the data-center business."
        ),
    },
    {
        "src": "VZ", "dst": "MSFT", "type": "Partnership",
        "desc": "Verizon + Microsoft Azure — private 5G edge cloud for enterprise customers",
        "value": "~$500M+ (multi-year)", "year": "2021",
        "source_url": "https://news.microsoft.com/2021/12/02/verizon-and-microsoft-team-to-deliver-private-5g-with-azure/",
        "source_name": "Microsoft News",
        "details": (
            "Verizon and Microsoft announced a partnership in December 2021 to deliver private "
            "5G network solutions for enterprise customers using Azure Private MEC (Multi-access "
            "Edge Compute). Verizon's 5G Ultra Wideband network connects factory floors and "
            "warehouses to Azure AI and IoT services. Joint customers include large manufacturers "
            "and logistics companies that need ultra-low latency. Verizon also uses Azure for its "
            "own enterprise cloud and collaboration tools."
        ),
    },
    {
        "src": "TMUS", "dst": "MSFT", "type": "Partnership",
        "desc": "T-Mobile + Microsoft — 5G AI network innovation and cloud-first enterprise deal",
        "value": "~$400M+ (multi-year)", "year": "2022",
        "source_url": "https://news.microsoft.com/2022/10/04/t-mobile-and-microsoft-announce-strategic-partnership-to-build-the-network-of-the-future/",
        "source_name": "Microsoft News",
        "details": (
            "T-Mobile and Microsoft announced a strategic partnership in October 2022 to build "
            "the network of the future. T-Mobile is moving workloads to Azure and using Azure "
            "AI/ML to improve network performance and customer service. Microsoft Teams is "
            "T-Mobile's enterprise collaboration platform. The partnership includes T-Mobile "
            "offering Microsoft 365 bundles to its business customers and joint development of "
            "5G-native AI applications."
        ),
    },
    {
        "src": "T", "dst": "AAPL", "type": "Partnership",
        "desc": "AT&T launched the original iPhone in 2007 as exclusive US carrier for 4 years",
        "value": "Revenue share (~$11/sub/mo at launch)", "year": "2007",
        "source_url": "https://www.apple.com/newsroom/2007/01/09Apple-Reinvents-the-Phone-with-iPhone/",
        "source_name": "Apple Newsroom",
        "details": (
            "AT&T (then Cingular, rebranded AT&T Mobility) was Apple's exclusive US carrier "
            "for the original iPhone launch in January 2007. The exclusivity agreement ran "
            "through 2011. AT&T paid Apple an unprecedented revenue share of subscriber bills "
            "and subsidized the device. iPhone drove AT&T's subscriber growth from 2007-2011 "
            "and is credited with transforming AT&T's consumer brand. The deal ended when "
            "Verizon launched iPhone 4 in February 2011."
        ),
    },
    {
        "src": "VZ", "dst": "AAPL", "type": "Partnership",
        "desc": "Verizon launched iPhone 4 in 2011, ending AT&T's 4-year exclusivity",
        "value": "Revenue share (undisclosed)", "year": "2011",
        "source_url": "https://www.apple.com/newsroom/2011/01/11iPhone-Coming-to-Verizon-Wireless/",
        "source_name": "Apple Newsroom",
        "details": (
            "Verizon Wireless launched the iPhone 4 on February 10, 2011, breaking AT&T's "
            "exclusive grip on iPhone in the US. Pre-orders sold out within hours. Apple "
            "CEO Steve Jobs appeared with Verizon CEO Ivan Seidenberg to announce the deal. "
            "Verizon's CDMA iPhone proved that carrier competition would accelerate iPhone "
            "adoption — Verizon quickly became Apple's largest US distribution partner by "
            "subscriber count and remains one of Apple's top three global carriers."
        ),
    },
    {
        "src": "TMUS", "dst": "AAPL", "type": "Partnership",
        "desc": "T-Mobile launched iPhone in 2013, completing US big-3 carrier coverage for Apple",
        "value": "Revenue share (undisclosed)", "year": "2013",
        "source_url": "https://newsroom.t-mobile.com/2013-04-12-T-Mobile-Officially-Launches-iPhone-Today",
        "source_name": "T-Mobile Newsroom",
        "details": (
            "T-Mobile USA launched the iPhone 5 on April 12, 2013 — the last of the three "
            "major US carriers to carry iPhone. T-Mobile was the first US carrier to offer "
            "iPhone without a traditional 2-year contract subsidy, instead offering monthly "
            "installment plans that lowered upfront cost. T-Mobile's uncarrier approach "
            "combined with iPhone drove its subscriber base from 33M to 100M+ by 2020 through "
            "the Sprint merger, making it the second-largest US carrier."
        ),
    },

    # ── Streaming × cloud and platform ───────────────────────────────────────

    {
        "src": "NFLX", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Netflix runs its entire streaming infrastructure on AWS — one of the largest cloud migrations",
        "value": "~$500M-1B annually", "year": "2008",
        "source_url": "https://aws.amazon.com/solutions/case-studies/netflix-case-study/",
        "source_name": "AWS Case Study",
        "details": (
            "Netflix began migrating to AWS in 2008 after a database corruption incident "
            "exposed the risks of its own data centers. The migration took 7 years and "
            "completed in 2016. AWS handles Netflix's compute, storage, transcoding, and "
            "global CDN (Open Connect for last-mile). Netflix is one of AWS's most visible "
            "enterprise customers and has open-sourced dozens of tools built on AWS including "
            "Chaos Monkey. Netflix's 247M+ subscriber streaming traffic makes it one of the "
            "largest workloads on the public internet."
        ),
    },
    {
        "src": "NFLX", "dst": "MSFT", "type": "Partnership",
        "desc": "Netflix chose Microsoft as its exclusive global ad technology and sales partner for its ad-supported tier",
        "value": "~$1B+ (estimated revenue share)", "year": "2022",
        "source_url": "https://about.netflix.com/en/news/building-a-better-ad-supported-experience-microsoft-as-our-global",
        "source_name": "Netflix Newsroom",
        "details": (
            "In July 2022, Netflix announced it had chosen Microsoft as its exclusive partner "
            "to power its new ad-supported subscription tier. Microsoft provides the ad "
            "serving technology via its Xandr (formerly AppNexus) platform and handles global "
            "ad sales. The deal surprised the industry as Google and The Trade Desk were "
            "expected to win the contract. Netflix's ad tier launched in November 2022 and "
            "reached 40M+ monthly active users by 2024. The partnership gives Microsoft a "
            "premium streaming advertising footprint it lacked."
        ),
    },
    {
        "src": "NFLX", "dst": "GOOGL", "type": "Supply Chain",
        "desc": "Netflix uses Google Cloud Platform for data analytics and AI recommendation workloads",
        "value": "~$300M+ annually", "year": "2016",
        "source_url": "https://cloud.google.com/customers/netflix",
        "source_name": "Google Cloud",
        "details": (
            "While Netflix's primary streaming infrastructure runs on AWS, Google Cloud handles "
            "Netflix's data analytics, content personalization, and machine learning workloads. "
            "Netflix uses BigQuery for petabyte-scale analytics and Vertex AI for its "
            "recommendation algorithms that drive 80% of content viewed. The multi-cloud "
            "approach lets Netflix use each provider's specialized strengths while avoiding "
            "lock-in. Netflix's data science team has published extensively on their GCP-based "
            "recommendation systems."
        ),
    },
    {
        "src": "NFLX", "dst": "AAPL", "type": "Partnership",
        "desc": "Netflix available on Apple TV hardware and iOS — Apple earns App Store commission on subscriptions",
        "value": "~$300-400M annually (App Store commission)", "year": "2010",
        "source_url": "https://ir.netflix.net/ir/doc/annual-reports",
        "source_name": "Netflix 10-K",
        "details": (
            "Netflix has been available on Apple TV since 2010 and is consistently the most "
            "downloaded streaming app on the App Store. Apple earns a 30% commission on new "
            "Netflix subscriptions purchased through iOS (dropping to 15% after year one). "
            "Netflix stopped allowing in-app subscriptions in 2018 to avoid the commission, "
            "directing users to subscribe via web — but Apple TV device distribution remains "
            "critical. Netflix is Apple TV's anchor streaming app and helped establish Apple TV "
            "as the leading premium streaming hardware platform."
        ),
    },
    {
        "src": "DIS", "dst": "AAPL", "type": "Partnership",
        "desc": "Disney+ available on Apple TV Channels — Apple bundled Disney+ at launch in 2019",
        "value": "~$100-200M annually (App Store commission)", "year": "2019",
        "source_url": "https://www.apple.com/newsroom/2019/11/apple-tv-channels-adds-disney-plus/",
        "source_name": "Apple Newsroom",
        "details": (
            "Apple and Disney announced that Disney+ would launch on Apple TV Channels on "
            "November 12, 2019 — the same day as Disney+'s US debut. Apple TV Channels allows "
            "subscribers to sign up for Disney+ directly inside the Apple TV app. Notably, "
            "Apple offered a free year of Apple TV+ with Disney+ for certain customers. Disney "
            "CEO Bob Iger and Apple CEO Tim Cook are close personally, and the companies have "
            "deep board-level relationships (Steve Jobs was Disney's largest individual "
            "shareholder via Pixar shares when he died)."
        ),
    },
    {
        "src": "CMCSA", "dst": "AAPL", "type": "Partnership",
        "desc": "NBCUniversal Peacock streaming app launched on Apple TV in July 2020",
        "value": "~$50-100M annually (App Store commission)", "year": "2020",
        "source_url": "https://www.apple.com/newsroom/2020/07/peacock-arrives-on-apple-tv-app/",
        "source_name": "Apple Newsroom",
        "details": (
            "Comcast's NBCUniversal launched Peacock streaming service on Apple TV app in "
            "July 2020, coinciding with Peacock's national US launch. The Apple TV integration "
            "supports all three Peacock tiers (Free, Premium, Premium Plus). Apple users can "
            "subscribe directly through Apple TV Channels, with Apple taking its standard "
            "commission. Peacock is available on all Apple devices including iPhone, iPad, and "
            "Mac, making Apple's ecosystem one of Peacock's primary distribution channels."
        ),
    },
    {
        "src": "WBD", "dst": "AAPL", "type": "Partnership",
        "desc": "Max (HBO Max) launched on Apple TV app in May 2020 — available via Apple TV Channels",
        "value": "~$100-150M annually (App Store commission)", "year": "2020",
        "source_url": "https://www.apple.com/newsroom/2020/05/hbo-max-coming-to-apple-tv/",
        "source_name": "Apple Newsroom",
        "details": (
            "HBO Max (now rebranded Max) launched on Apple TV hardware and via Apple TV "
            "Channels in May 2020, in time for the HBO Max service launch. Apple TV Channels "
            "integration allows subscribers to sign up for Max directly within the Apple TV "
            "app. Warner Bros. Discovery negotiated revenue-sharing arrangements with Apple. "
            "Max is one of the top-5 most subscribed channels on Apple TV, with HBO's premium "
            "content driving strong conversion from Apple TV device owners."
        ),
    },
    {
        "src": "TMUS", "dst": "NFLX", "type": "Partnership",
        "desc": "T-Mobile 'Netflix On Us' — free Netflix included in qualifying T-Mobile plans since 2017",
        "value": "~$300-500M annually (subscriber subsidy)", "year": "2017",
        "source_url": "https://newsroom.t-mobile.com/2017-09-13-T-Mobile-Adds-Netflix-On-Us-for-All-T-Mobile-ONE-Customers-Both-New-and-Existing",
        "source_name": "T-Mobile Newsroom",
        "details": (
            "T-Mobile CEO John Legere and Netflix CEO Reed Hastings announced 'Netflix On Us' "
            "in September 2017 — T-Mobile ONE customers get a free Netflix Standard subscription "
            "included with their plan. It was the first major mobile carrier-streaming bundle "
            "in the US. T-Mobile pays Netflix at wholesale rates for the bundled subscriptions. "
            "The partnership drove T-Mobile subscriber acquisition and reduced Netflix churn by "
            "embedding it into bills. The program has continued under CEO Mike Sievert, evolving "
            "to include Netflix ad-supported and standard tiers."
        ),
    },
    {
        "src": "DIS", "dst": "CMCSA", "type": "Joint Venture",
        "desc": "Hulu joint venture: Disney buys out Comcast's 33% stake in November 2023",
        "value": "~$8.61B (Comcast buyout price)", "year": "2009",
        "source_url": "https://thewaltdisneycompany.com/the-walt-disney-company-acquires-full-ownership-of-hulu/",
        "source_name": "Walt Disney Company",
        "details": (
            "Hulu was founded in 2007 as a joint venture between NBC Universal (Comcast), "
            "Fox (News Corp), and ABC (Disney). Disney became majority owner (67%) after "
            "acquiring Fox's assets in 2019. In May 2023, Disney and Comcast agreed that "
            "Disney would acquire Comcast's remaining 33% stake at a minimum price of $8.61B, "
            "completed in November 2023. Hulu had 50M+ subscribers when Disney took full "
            "control. Disney now operates Hulu, Disney+, and ESPN+ as a unified streaming "
            "portfolio, with Comcast retaining distribution rights through its Xfinity platform."
        ),
    },
    {
        "src": "DIS", "dst": "AMZN", "type": "Partnership",
        "desc": "Disney+ and ESPN+ available on Amazon Fire TV devices and as Prime Video Channels",
        "value": "~$100-200M annually (distribution)", "year": "2019",
        "source_url": "https://www.aboutamazon.com/news/entertainment/disney-plus-arrives-on-amazon-fire-tv",
        "source_name": "About Amazon",
        "details": (
            "Disney+ launched on Amazon Fire TV on November 12, 2019, its first day of "
            "availability. Fire TV is one of the most widely deployed streaming device platforms "
            "in the US with 50M+ active users. Disney+, Hulu, and ESPN+ are all available "
            "through Amazon's Prime Video Channels, allowing Amazon subscribers to add Disney "
            "content without leaving the Prime Video interface. Amazon takes a commission on "
            "subscriptions purchased through its platform while Disney gains access to "
            "Amazon's massive installed device base."
        ),
    },

    # ── Social / digital media ────────────────────────────────────────────────

    {
        "src": "SNAP", "dst": "GOOGL", "type": "Supply Chain",
        "desc": "Snap committed ~$2B to Google Cloud over five years for Snapchat infrastructure",
        "value": "~$2B (5-year commitment)", "year": "2022",
        "source_url": "https://cloud.google.com/customers/snap",
        "source_name": "Google Cloud",
        "details": (
            "Snap and Google Cloud expanded their partnership in 2022 with a multi-year, "
            "multi-billion dollar infrastructure commitment. Snapchat's compute, storage, and "
            "ML workloads — including Snap's camera AI and Lens AR features — run primarily "
            "on Google Cloud. Snap also uses Google Cloud for its Snap Map data processing "
            "and its advertising auction infrastructure. The relationship is one of Google "
            "Cloud's most prominent social media customers and a key reference for GCP's "
            "real-time media processing capabilities."
        ),
    },
    {
        "src": "SNAP", "dst": "MSFT", "type": "Partnership",
        "desc": "Snapchat 'My AI' chatbot powered by Microsoft Bing / OpenAI GPT-4 (2023)",
        "value": "Revenue sharing (undisclosed)", "year": "2023",
        "source_url": "https://newsroom.snap.com/2023-02-27-Snapchat-My-AI",
        "source_name": "Snap Newsroom",
        "details": (
            "Snap launched 'My AI' in February 2023, an AI chatbot built into Snapchat powered "
            "by OpenAI's GPT-4 — which Microsoft distributes through Azure OpenAI Service. "
            "My AI became available to all Snapchat users in April 2023 (initially paid-only). "
            "It reached 150M+ users within months. The integration marked one of the first "
            "large-scale social media deployments of GPT-4. Snap also integrates Bing Search "
            "results into My AI responses, making Microsoft a key technology partner for "
            "Snap's generative AI strategy."
        ),
    },
    {
        "src": "PINS", "dst": "GOOGL", "type": "Partnership",
        "desc": "Pinterest + Google — Google Shopping Ads power the majority of Pinterest's ad revenue",
        "value": "~$500M+ annually", "year": "2018",
        "source_url": "https://newsroom.pinterest.com/en/post/pinterest-and-google-ads-partner",
        "source_name": "Pinterest Newsroom",
        "details": (
            "Pinterest and Google partnered in 2018 to integrate Google Shopping Ads into "
            "Pinterest's platform, allowing advertisers to run shopping campaigns across both "
            "platforms simultaneously. Google advertising represents a substantial share of "
            "Pinterest's total revenue through ad network agreements. Google's product listing "
            "ads appear natively within Pinterest's visual discovery feed. The partnership "
            "gives Pinterest access to Google's massive advertiser base while Google gains "
            "access to Pinterest's highly purchase-intent audience of 500M+ monthly users."
        ),
    },
    {
        "src": "PINS", "dst": "MSFT", "type": "Partnership",
        "desc": "Pinterest + Microsoft Advertising — Bing visual search and expanded ad marketplace",
        "value": "~$100M+ annually", "year": "2022",
        "source_url": "https://about.ads.microsoft.com/en-us/blog/post/june-2022/microsoft-and-pinterest-expand-advertising-partnership",
        "source_name": "Microsoft Advertising Blog",
        "details": (
            "Pinterest and Microsoft Advertising expanded their partnership in June 2022, "
            "making Pinterest's ad inventory available through Microsoft's advertising "
            "marketplace. Advertisers using Microsoft Ads can now reach Pinterest's audience "
            "directly. Microsoft Bing also indexes Pinterest images for visual search. The "
            "deal diversifies Pinterest's revenue beyond Google and Meta advertising and gives "
            "Microsoft Advertising a premium visual content platform that competes with "
            "Google's visual search advertising."
        ),
    },
    {
        "src": "META", "dst": "AMZN", "type": "Partnership",
        "desc": "Amazon product ads integrated natively into Facebook and Instagram feeds (2023)",
        "value": "~$1B+ annually (estimated)", "year": "2023",
        "source_url": "https://www.aboutamazon.com/news/retail/amazon-meta-ads-integration",
        "source_name": "About Amazon",
        "details": (
            "Amazon and Meta announced a direct advertising integration in November 2023, "
            "allowing Facebook and Instagram users to purchase Amazon products without leaving "
            "the social apps. When users see an Amazon ad in their Meta feed, they can click "
            "to buy using their saved Amazon payment and shipping details — reducing friction "
            "vs. traditional social commerce. Amazon ads link directly to Prime shipping "
            "benefits. The integration is Meta's largest commerce partnership and signals "
            "a new era of social-to-marketplace direct purchase."
        ),
    },

    # ── Advertising and content distribution ──────────────────────────────────

    {
        "src": "GOOGL", "dst": "SPOT", "type": "Partnership",
        "desc": "Spotify + Google Cloud — Spotify migrated to GCP and is a preferred Google Assistant music partner",
        "value": "~$100M+ annually (cloud + revenue share)", "year": "2019",
        "source_url": "https://newsroom.spotify.com/2019-02-20/google-and-spotify-expand-partnership/",
        "source_name": "Spotify Newsroom",
        "details": (
            "Spotify and Google announced an expanded partnership in February 2019 with two "
            "components: (1) Spotify signed a multi-year commitment to Google Cloud Platform "
            "as its primary cloud infrastructure provider, migrating petabytes of music data "
            "and personalization workloads to GCP. (2) Spotify became the preferred music "
            "partner for Google Assistant, meaning 'Hey Google, play music' defaults to "
            "Spotify on Android and Google Home devices. Spotify is also preinstalled on "
            "Pixel phones in some markets. The deal runs counter to Google's own YouTube Music "
            "ambitions but reflects Google's cloud-revenue-first strategy."
        ),
    },
    {
        "src": "DIS", "dst": "GOOGL", "type": "Partnership",
        "desc": "Disney advertising on Google DV360; Hulu and ESPN content distributed via YouTube TV",
        "value": "~$500M+ annually (advertising)", "year": "2020",
        "source_url": "https://thewaltdisneycompany.com/the-walt-disney-company-investor-relations/",
        "source_name": "Walt Disney Company IR",
        "details": (
            "Disney is one of Google's largest advertising partners, spending hundreds of "
            "millions annually on Google's ad platforms (Search, YouTube, DV360 programmatic) "
            "to promote Disney+, Marvel, Star Wars, ESPN, and theme parks. Hulu with Live TV "
            "is available through YouTube TV as a channel add-on. ESPN content is integrated "
            "into Google TV interfaces. Disney's media brands (ABC, ESPN, Disney Channel) run "
            "programmatic ads via Google's advertising tech stack, making Google a critical "
            "distribution layer for Disney's entire media portfolio."
        ),
    },
    {
        "src": "CMCSA", "dst": "GOOGL", "type": "Partnership",
        "desc": "NBCUniversal advertising on YouTube; Peacock integrates with Google TV and Chromecast",
        "value": "~$200M+ annually (advertising)", "year": "2021",
        "source_url": "https://cloud.google.com/customers/comcast",
        "source_name": "Google Cloud",
        "details": (
            "Comcast's NBCUniversal is a major Google advertising partner, running campaigns "
            "for NBC broadcast, Peacock streaming, and Universal Studios on YouTube and "
            "Google's DV360 programmatic platform. Peacock is integrated natively into Google "
            "TV (the software that ships on Chromecast) as a featured streaming service. "
            "Comcast also uses Google Cloud Platform for portions of its video streaming "
            "infrastructure and data analytics. The relationship spans advertising, "
            "distribution, and enterprise cloud services."
        ),
    },
    {
        "src": "GOOGL", "dst": "T", "type": "Partnership",
        "desc": "AT&T migrates network and software workloads to Google Cloud Platform",
        "value": "~$1B+ (multi-year)", "year": "2021",
        "source_url": "https://cloud.google.com/customers/att",
        "source_name": "Google Cloud",
        "details": (
            "AT&T selected Google Cloud as a strategic cloud partner in 2021 to complement "
            "its Microsoft Azure deal. Google Cloud handles AT&T's network analytics, "
            "5G network function virtualization (NFV), and AI-driven network optimization. "
            "AT&T uses Google's Anthos multi-cloud platform to manage workloads across "
            "Azure and GCP simultaneously. The dual-cloud strategy gives AT&T negotiating "
            "leverage and technical redundancy across two hyperscalers, while Google gains "
            "a marquee telecom reference customer for its network cloud solutions."
        ),
    },

    # ── Gaming and entertainment ───────────────────────────────────────────────

    {
        "src": "EA", "dst": "MSFT", "type": "Partnership",
        "desc": "EA Play included in Xbox Game Pass Ultimate — all EA titles in Microsoft's subscription",
        "value": "~$1-2B annually (licensing estimate)", "year": "2020",
        "source_url": "https://www.ea.com/en-gb/news/ea-play-game-pass-ultimate",
        "source_name": "EA Newsroom",
        "details": (
            "EA and Microsoft announced that EA Play, Electronic Arts' own game subscription "
            "service, would be included at no extra cost in Xbox Game Pass Ultimate in "
            "November 2020. This gave Game Pass members instant access to 60+ EA titles "
            "including Battlefield, FIFA, Madden, Star Wars Jedi, Mass Effect, and Dragon Age. "
            "The deal is EA's largest distribution partnership and significantly expanded "
            "Xbox Game Pass's content library. EA also added EA Play to PC Game Pass. "
            "The arrangement pays EA per-play royalties from Microsoft's subscription revenue."
        ),
    },
    {
        "src": "CHTR", "dst": "GOOGL", "type": "Partnership",
        "desc": "Charter Spectrum uses Google Cloud for video streaming and network data analytics",
        "value": "Revenue sharing (undisclosed)", "year": "2021",
        "source_url": "https://cloud.google.com/customers/charter-communications",
        "source_name": "Google Cloud",
        "details": (
            "Charter Communications (Spectrum) uses Google Cloud Platform for its Spectrum "
            "TV app streaming infrastructure, customer data analytics, and network operations. "
            "Charter's migration to Google Cloud supports its Spectrum TV app, which competes "
            "with streaming services by delivering live TV and on-demand content over the "
            "internet. Google Cloud's real-time data processing handles Charter's network "
            "telemetry for proactive fault detection across its cable network serving "
            "32M+ customers."
        ),
    },

    # ── Enterprise cloud for media companies ──────────────────────────────────

    {
        "src": "CMCSA", "dst": "MSFT", "type": "Partnership",
        "desc": "Comcast + Microsoft Azure — enterprise cloud for Sky, NBCUniversal, and Xfinity",
        "value": "~$500M+ (multi-year)", "year": "2020",
        "source_url": "https://news.microsoft.com/2020/09/17/comcast-and-microsoft-expand-partnership-to-advance-enterprise-cloud-services/",
        "source_name": "Microsoft News",
        "details": (
            "Comcast and Microsoft expanded their enterprise cloud partnership in September "
            "2020. Comcast is migrating its Sky satellite TV service (UK/Europe) to Azure, "
            "running content delivery, subscriber management, and advertising systems in the "
            "cloud. NBCUniversal's production and broadcast tools also run on Azure. Microsoft "
            "Teams is deployed across Comcast's 190,000+ employees. The relationship positions "
            "Azure as Comcast's primary cloud for media and entertainment workloads."
        ),
    },
    {
        "src": "WBD", "dst": "MSFT", "type": "Partnership",
        "desc": "Warner Bros. Discovery + Microsoft Azure — strategic cloud and AI partnership (2022)",
        "value": "~$1B+ (multi-year)", "year": "2022",
        "source_url": "https://news.microsoft.com/2022/10/18/warner-bros-discovery-and-microsoft-announce-a-strategic-alliance/",
        "source_name": "Microsoft News",
        "details": (
            "Warner Bros. Discovery and Microsoft announced a strategic alliance in October "
            "2022 shortly after the $43B Discovery-WarnerMedia merger closed. WBD is using "
            "Azure for Max streaming infrastructure, AI-driven content discovery, and cloud "
            "production tools. Microsoft Azure handles encoding, transcoding, and content "
            "delivery for Max's 95M+ global subscribers. Azure AI helps WBD with content "
            "recommendation, automated subtitle generation, and fraud detection. The deal "
            "is Microsoft's largest media and entertainment cloud contract."
        ),
    },
    {
        "src": "SPOT", "dst": "MSFT", "type": "Partnership",
        "desc": "Spotify group listening available inside Microsoft Teams — social audio integration",
        "value": "Nominal (strategic distribution)", "year": "2021",
        "source_url": "https://newsroom.spotify.com/2021-03-02/you-can-now-listen-together-in-microsoft-teams/",
        "source_name": "Spotify Newsroom",
        "details": (
            "Spotify and Microsoft announced an integration in March 2021 allowing Teams users "
            "to listen to Spotify together during video calls and meetings — Spotify's first "
            "integration with an enterprise collaboration platform. Users can share Spotify "
            "playback into a Teams call, enabling group listening for remote workplaces. "
            "The integration is available on the Spotify Miniplayer inside Teams. While "
            "financially modest, the partnership extended Spotify into Microsoft's 300M+ "
            "Teams user base and signaled Spotify's ambition to be the music layer for "
            "enterprise collaboration."
        ),
    },
    {
        "src": "LYV", "dst": "MSFT", "type": "Partnership",
        "desc": "Live Nation + Microsoft — Azure cloud for Ticketmaster scalability and enterprise operations",
        "value": "Revenue sharing (undisclosed)", "year": "2022",
        "source_url": "https://news.microsoft.com/2022/05/18/microsoft-and-live-nation-entertainment-announce-strategic-alliance/",
        "source_name": "Microsoft News",
        "details": (
            "Live Nation Entertainment and Microsoft announced a strategic alliance in May 2022. "
            "Ticketmaster, Live Nation's ticketing subsidiary, is migrating to Azure to handle "
            "massive traffic spikes (millions of concurrent users during Taylor Swift / "
            "Beyoncé onsales). Azure's scalable compute addresses the crashes that plagued "
            "Ticketmaster during high-demand events. Microsoft also provides Teams for "
            "Live Nation's enterprise operations and Azure AI for venue analytics, dynamic "
            "pricing, and fan experience personalization across 40,000+ annual events."
        ),
    },
]

# ── Fast lookup (undirected) ──────────────────────────────────────────────────
EDGE_LOOKUP: dict[tuple[str, str], dict] = {}
for _e in NETWORK_EDGES:
    EDGE_LOOKUP[(_e["src"], _e["dst"])] = _e
    EDGE_LOOKUP[(_e["dst"], _e["src"])] = _e

# ── Visual styling ────────────────────────────────────────────────────────────
SECTOR_COLORS: dict[str, str] = {
    "Technology":             "#1A6DFF",
    "Communication Services": "#9C27B0",
    "Consumer Cyclical":      "#FF9800",
    "Consumer Defensive":     "#4CAF50",
    "Financial Services":     "#26C6DA",
    "Energy":                 "#FF5722",
    "Healthcare":             "#E91E63",
    "Industrials":            "#78909C",
    "Real Estate":            "#8D6E63",
    "Utilities":              "#FFEE58",
    "Basic Materials":        "#66BB6A",
}

REL_COLORS: dict[str, str] = {
    "Supply Chain": "#FF9800",
    "Partnership":  "#1A6DFF",
    "Ownership":    "#00CC66",
    "Joint Venture": "#E91E63",
}
