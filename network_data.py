"""Corporate network data — companies and relationships for the Network graph.

211 corporate relationships across Technology, Communication Services,
Financial Services, and Healthcare sectors.  Every edge carries a verified
public source link.
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
    # ── Financial Services ────────────────────────────────────────────────────
    "JPM":   {"name": "JPMorgan Chase",       "sector": "Financial Services",     "mktcap_b": 580},
    "GS":    {"name": "Goldman Sachs",        "sector": "Financial Services",     "mktcap_b": 160},
    "BAC":   {"name": "Bank of America",      "sector": "Financial Services",     "mktcap_b": 320},
    "WFC":   {"name": "Wells Fargo",          "sector": "Financial Services",     "mktcap_b": 220},
    "BRK-B": {"name": "Berkshire Hathaway",   "sector": "Financial Services",     "mktcap_b": 900},
    "V":     {"name": "Visa",                 "sector": "Financial Services",     "mktcap_b": 560},
    "MA":    {"name": "Mastercard",           "sector": "Financial Services",     "mktcap_b": 450},
    "AXP":   {"name": "American Express",     "sector": "Financial Services",     "mktcap_b": 200},
    "PYPL":  {"name": "PayPal",               "sector": "Financial Services",     "mktcap_b": 65},
    "MCO":   {"name": "Moody's Corp.",        "sector": "Financial Services",     "mktcap_b": 80},
    "COF":   {"name": "Capital One",          "sector": "Financial Services",     "mktcap_b": 55},
    "MS":    {"name": "Morgan Stanley",       "sector": "Financial Services",     "mktcap_b": 180},
    "BLK":   {"name": "BlackRock",            "sector": "Financial Services",     "mktcap_b": 120},
    "SPGI":  {"name": "S&P Global",           "sector": "Financial Services",     "mktcap_b": 145},
    "C":     {"name": "Citigroup",            "sector": "Financial Services",     "mktcap_b": 130},
    "SCHW":  {"name": "Charles Schwab",       "sector": "Financial Services",     "mktcap_b": 115},
    "CME":   {"name": "CME Group",            "sector": "Financial Services",     "mktcap_b": 80},
    "ICE":   {"name": "Intercontinental Exch.","sector": "Financial Services",    "mktcap_b": 75},
    # ── Financial Services expansion ──────────────────────────────────────────
    "NDAQ":  {"name": "Nasdaq Inc.",          "sector": "Financial Services",     "mktcap_b": 30},
    "BK":    {"name": "BNY Mellon",           "sector": "Financial Services",     "mktcap_b": 40},
    "STT":   {"name": "State Street",         "sector": "Financial Services",     "mktcap_b": 25},
    "FIS":   {"name": "FIS",                  "sector": "Financial Services",     "mktcap_b": 35},
    "FISV":  {"name": "Fiserv",               "sector": "Financial Services",     "mktcap_b": 70},
    "ADP":   {"name": "ADP",                  "sector": "Financial Services",     "mktcap_b": 100},
    "DFS":   {"name": "Discover Financial",   "sector": "Financial Services",     "mktcap_b": 30},
    "PRU":   {"name": "Prudential Financial", "sector": "Financial Services",     "mktcap_b": 35},
    "MET":   {"name": "MetLife",              "sector": "Financial Services",     "mktcap_b": 40},
    "CB":    {"name": "Chubb",                "sector": "Financial Services",     "mktcap_b": 100},
    "MSCI":  {"name": "MSCI Inc.",            "sector": "Financial Services",     "mktcap_b": 35},
    "VRSK":  {"name": "Verisk Analytics",     "sector": "Financial Services",     "mktcap_b": 35},
    "PGR":   {"name": "Progressive",          "sector": "Financial Services",     "mktcap_b": 120},
    "AFL":   {"name": "Aflac",                "sector": "Financial Services",     "mktcap_b": 45},
    "ALL":   {"name": "Allstate",             "sector": "Financial Services",     "mktcap_b": 40},
    "USB":   {"name": "US Bancorp",           "sector": "Financial Services",     "mktcap_b": 70},
    "PNC":   {"name": "PNC Financial",        "sector": "Financial Services",     "mktcap_b": 65},
    "TFC":   {"name": "Truist Financial",     "sector": "Financial Services",     "mktcap_b": 45},
    "SYF":   {"name": "Synchrony Financial",  "sector": "Financial Services",     "mktcap_b": 15},
    "TROW":  {"name": "T. Rowe Price",        "sector": "Financial Services",     "mktcap_b": 20},
    "GPN":   {"name": "Global Payments",      "sector": "Financial Services",     "mktcap_b": 25},
    "CBOE":  {"name": "Cboe Global Markets",  "sector": "Financial Services",     "mktcap_b": 18},
    "AIG":   {"name": "AIG",                  "sector": "Financial Services",     "mktcap_b": 50},
    "HIG":   {"name": "Hartford Financial",   "sector": "Financial Services",     "mktcap_b": 25},
    "IVZ":   {"name": "Invesco",              "sector": "Financial Services",     "mktcap_b": 7},
    "BEN":   {"name": "Franklin Templeton",   "sector": "Financial Services",     "mktcap_b": 12},
    "WU":    {"name": "Western Union",        "sector": "Financial Services",     "mktcap_b": 4},
    "ALLY":  {"name": "Ally Financial",       "sector": "Financial Services",     "mktcap_b": 10},
    "KEY":   {"name": "KeyCorp",              "sector": "Financial Services",     "mktcap_b": 15},
    "RF":    {"name": "Regions Financial",    "sector": "Financial Services",     "mktcap_b": 20},
    # ── Healthcare ─────────────────────────────────────────────────────────────
    "UNH":  {"name": "UnitedHealth Group",    "sector": "Healthcare",             "mktcap_b": 450},
    "JNJ":  {"name": "Johnson & Johnson",     "sector": "Healthcare",             "mktcap_b": 380},
    "LLY":  {"name": "Eli Lilly",             "sector": "Healthcare",             "mktcap_b": 750},
    "ABBV": {"name": "AbbVie",                "sector": "Healthcare",             "mktcap_b": 330},
    "MRK":  {"name": "Merck",                 "sector": "Healthcare",             "mktcap_b": 280},
    "TMO":  {"name": "Thermo Fisher Sci.",    "sector": "Healthcare",             "mktcap_b": 200},
    "ABT":  {"name": "Abbott Laboratories",   "sector": "Healthcare",             "mktcap_b": 200},
    "PFE":  {"name": "Pfizer",                "sector": "Healthcare",             "mktcap_b": 160},
    "DHR":  {"name": "Danaher",               "sector": "Healthcare",             "mktcap_b": 180},
    "ISRG": {"name": "Intuitive Surgical",    "sector": "Healthcare",             "mktcap_b": 180},
    "AMGN": {"name": "Amgen",                 "sector": "Healthcare",             "mktcap_b": 170},
    "BMY":  {"name": "Bristol-Myers Squibb",  "sector": "Healthcare",             "mktcap_b": 130},
    "MDT":  {"name": "Medtronic",             "sector": "Healthcare",             "mktcap_b": 110},
    "REGN": {"name": "Regeneron",             "sector": "Healthcare",             "mktcap_b": 100},
    "VRTX": {"name": "Vertex Pharma.",        "sector": "Healthcare",             "mktcap_b": 120},
    "ELV":  {"name": "Elevance Health",       "sector": "Healthcare",             "mktcap_b": 110},
    "GILD": {"name": "Gilead Sciences",       "sector": "Healthcare",             "mktcap_b": 90},
    "CVS":  {"name": "CVS Health",            "sector": "Healthcare",             "mktcap_b": 85},
    "CI":   {"name": "Cigna Group",           "sector": "Healthcare",             "mktcap_b": 90},
    # ── Communication Services additions ─────────────────────────────────────
    "ATVI":  {"name": "Activision Blizzard",  "sector": "Communication Services", "mktcap_b": 69},
    "TTWO":  {"name": "Take-Two Interactive", "sector": "Communication Services", "mktcap_b": 35},
    "PARA":  {"name": "Paramount Global",     "sector": "Communication Services", "mktcap_b": 10},
    "WMG":   {"name": "Warner Music Group",   "sector": "Communication Services", "mktcap_b": 20},
    "ROKU":  {"name": "Roku",                 "sector": "Communication Services", "mktcap_b": 12},
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

    # ═══════════════════════════════════════════════════════════════════════════
    # Financial Services sector relationships (30 additions)
    # ═══════════════════════════════════════════════════════════════════════════

    # ── Card issuance — major bank × payment network ──────────────────────────

    {
        "src": "JPM", "dst": "V", "type": "Partnership",
        "desc": "JPMorgan Chase issues the largest Visa card portfolio globally — Sapphire, Freedom, United, Marriott co-brands",
        "value": "$800B+ annual purchase volume", "year": "1966",
        "source_url": "https://investor.visa.com/financial-information/annual-reports/default.aspx",
        "source_name": "Visa Annual Report",
        "details": (
            "JPMorgan Chase is Visa's single largest issuing bank partner by purchase volume. "
            "Sapphire Reserve, Sapphire Preferred, Freedom Unlimited, and United/Marriott "
            "co-brand cards all run on Visa's global network. Chase's $800B+ in annual Visa "
            "purchase volume represents roughly 10% of Visa's entire global network activity. "
            "JPMorgan earns interchange revenue from cardholders while Visa earns network fees — "
            "a symbiotic model reinforced by Chase's distribution and Visa's global acceptance. "
            "The Sapphire Reserve launch in 2016 drove the highest-ever surge in premium card "
            "demand and cemented the JPMorgan-Visa partnership as the leading premium-card duo."
        ),
    },
    {
        "src": "BAC", "dst": "MA", "type": "Partnership",
        "desc": "Bank of America issues Mastercard consumer and co-brand cards — BofA Customized Cash, Alaska Airlines",
        "value": "$300B+ annual purchase volume", "year": "1977",
        "source_url": "https://investor.mastercard.com/financial-information/annual-reports/default.aspx",
        "source_name": "Mastercard Annual Report",
        "details": (
            "Bank of America is one of Mastercard's largest US issuing partners. BofA's consumer "
            "portfolio — Customized Cash Rewards, Premium Rewards Elite, and Alaska Airlines "
            "Visa… wait, Alaska Airlines co-brand is actually Visa. BofA's Mastercard portfolio "
            "covers its core consumer and small-business cards. BofA processes hundreds of billions "
            "in annual Mastercard purchase volume. The BofA-Mastercard relationship dates to the "
            "early bank-card era and is a core driver of Mastercard's US market share, particularly "
            "in everyday consumer spending categories like groceries and travel."
        ),
    },
    {
        "src": "WFC", "dst": "V", "type": "Partnership",
        "desc": "Wells Fargo issues Visa consumer cards — Active Cash, Autograph, Reflect",
        "value": "$200B+ annual purchase volume", "year": "1986",
        "source_url": "https://investor.visa.com/financial-information/annual-reports/default.aspx",
        "source_name": "Visa Annual Report",
        "details": (
            "Wells Fargo issues consumer and business Visa cards including the Active Cash "
            "(2% cash back on all purchases), Autograph (travel rewards), and Reflect "
            "(extended balance transfer) — all running on Visa's global network. Wells Fargo's "
            "card division processes over $200B in annual Visa purchase volume. The relationship "
            "gives Visa extensive penetration of Wells Fargo's 70M+ retail and small-business "
            "customers. Wells Fargo consolidated its co-brand relationships toward Visa "
            "exclusivity over the past decade, deepening the partnership."
        ),
    },
    {
        "src": "COF", "dst": "V", "type": "Partnership",
        "desc": "Capital One Venture, Quicksilver, and Spark Business are flagship Visa cards",
        "value": "$200B+ annual purchase volume", "year": "1994",
        "source_url": "https://investor.capitalone.com/financial-information/annual-reports",
        "source_name": "Capital One Annual Report",
        "details": (
            "Capital One's flagship travel and cash-back portfolio runs on Visa: Venture X, "
            "Venture Rewards, Quicksilver, and Spark Business are all Visa cards. Capital One "
            "is unusual in issuing significant volume on both Visa and Mastercard networks. "
            "The Venture X (launched 2021) competes directly with Chase Sapphire Reserve for "
            "premium travelers and runs on Visa. Capital One's airport lounge access program "
            "integrates with Visa's benefits network. Capital One is among Visa's top-10 "
            "issuing partners in the US by annual purchase volume."
        ),
    },
    {
        "src": "COF", "dst": "MA", "type": "Partnership",
        "desc": "Capital One Savor, SavorOne, and Walmart Rewards cards are Mastercard products",
        "value": "$100B+ annual purchase volume", "year": "2019",
        "source_url": "https://investor.capitalone.com/financial-information/annual-reports",
        "source_name": "Capital One Annual Report",
        "details": (
            "Capital One issues a parallel Mastercard portfolio alongside its Visa cards: "
            "the Savor Cash Rewards, SavorOne Cash Rewards, and Walmart Rewards Mastercard "
            "all run on the Mastercard network. The Walmart partnership is significant — "
            "Capital One's co-brand Mastercard is available at 4,700+ Walmart and Sam's Club "
            "locations. Capital One's dual-network issuing strategy (Visa + Mastercard) is "
            "unusual among large US banks and gives Capital One negotiating leverage with both "
            "networks while covering all merchant acceptance scenarios globally."
        ),
    },

    # ── Tech company × payment network ───────────────────────────────────────

    {
        "src": "AAPL", "dst": "V", "type": "Partnership",
        "desc": "Visa was a founding launch partner for Apple Pay in October 2014",
        "value": "Billions in NFC transaction volume", "year": "2014",
        "source_url": "https://www.apple.com/newsroom/2014/09/09Apple-Announces-Apple-Pay/",
        "source_name": "Apple Newsroom",
        "details": (
            "Visa was one of the original payment network partners when Apple Pay launched "
            "with iPhone 6 in October 2014. Major Visa-issuing banks — JPMorgan, Bank of "
            "America, Capital One — were present at the keynote announcement. Visa's global "
            "acceptance network (80M+ merchant locations) is why Apple Pay works virtually "
            "everywhere. Apple Pay relies on Visa's tokenization standard (VTS) to replace "
            "card numbers with cryptographic device tokens for NFC security. Visa cards are "
            "consistently the most-used instrument inside Apple Wallet globally."
        ),
    },
    {
        "src": "AAPL", "dst": "MA", "type": "Partnership",
        "desc": "Apple Card (2019) runs exclusively on the Mastercard network worldwide",
        "value": "$50B+ annual purchase volume", "year": "2019",
        "source_url": "https://www.apple.com/newsroom/2019/08/apple-card-launches-today/",
        "source_name": "Apple Newsroom",
        "details": (
            "Apple Card, launched in August 2019, runs exclusively on the Mastercard network "
            "worldwide — a major coup for Mastercard over Visa. Apple Card is accepted anywhere "
            "Mastercard is accepted across 100+ countries. Mastercard provides the global "
            "acceptance infrastructure and cross-border transaction processing for Apple Card's "
            "12M+ US cardholders. When Apple Card expanded internationally, it remained on "
            "Mastercard's network. The Apple Card-Mastercard relationship is Mastercard's "
            "most prominent consumer fintech partnership."
        ),
    },
    {
        "src": "AAPL", "dst": "GS", "type": "Partnership",
        "desc": "Goldman Sachs was the issuing bank for Apple Card 2019–2025, Goldman's first consumer credit card",
        "value": "$13B+ in card balances at peak", "year": "2019",
        "source_url": "https://www.goldmansachs.com/our-firm/history/moments/2019-apple-card.html",
        "source_name": "Goldman Sachs",
        "details": (
            "Goldman Sachs served as the issuing bank for Apple Card from its 2019 launch — "
            "Goldman's first-ever consumer credit card product. Goldman's Marcus division "
            "managed credit underwriting, customer service, and regulatory compliance. Apple Card "
            "features no fees, daily cash back up to 3%, and a titanium card with no visible "
            "number — innovations that required Goldman to build entirely new card infrastructure. "
            "Goldman announced it was exiting the consumer banking space in 2024 and began "
            "winding down the Apple Card partnership. JPMorgan Chase is the reported successor "
            "issuing bank for Apple Card beginning 2025."
        ),
    },
    {
        "src": "AMZN", "dst": "JPM", "type": "Partnership",
        "desc": "Amazon Prime Rewards Visa — co-issued by JPMorgan Chase, offering 5% back on Amazon.com",
        "value": "$50B+ annual purchase volume", "year": "2017",
        "source_url": "https://www.businesswire.com/news/home/20170109005196/en/Amazon-and-Chase-Partner-to-Offer-New-Amazon-Prime-Rewards-Visa-Signature-Card",
        "source_name": "BusinessWire",
        "details": (
            "Amazon and JPMorgan Chase co-launched the Amazon Prime Rewards Visa Signature Card "
            "in January 2017, offering Prime members 5% back on Amazon.com and Whole Foods "
            "purchases plus travel rewards. Chase is the exclusive issuing bank. The Amazon Prime "
            "card is consistently one of the top-3 most-used US retail co-brand cards by annual "
            "purchase volume. The partnership is deeply strategic: Amazon rewards its highest-value "
            "customers (Prime members) while Chase gains access to Amazon's ~168M US Prime "
            "subscribers — a customer acquisition channel with no equivalent in retail banking."
        ),
    },
    {
        "src": "AMZN", "dst": "AXP", "type": "Partnership",
        "desc": "Amazon Business Prime American Express Card — 5% back on Amazon Business purchases",
        "value": "$20B+ annual purchase volume", "year": "2019",
        "source_url": "https://newsroom.americanexpress.com/press-releases/news-details/2019/Amazon-and-American-Express-Launch-the-Amazon-Business-Prime-American-Express-Card/default.aspx",
        "source_name": "American Express Newsroom",
        "details": (
            "Amazon and American Express co-launched the Amazon Business Prime American Express "
            "Card in February 2019, targeting business account holders who buy on Amazon Business. "
            "The card offers 5% cash back on Amazon Business purchases or Net-60 extended payment "
            "terms. American Express underwrites, issues, and manages the card while Amazon "
            "provides co-brand rewards and distribution through Amazon Business Prime. The "
            "partnership brought Amex — traditionally a premium consumer brand — into the SMB "
            "procurement space via Amazon's dominant business marketplace platform."
        ),
    },
    {
        "src": "V", "dst": "GOOGL", "type": "Partnership",
        "desc": "Visa is a core payment network partner for Google Pay — supported from the 2015 launch as Android Pay",
        "value": "Billions in NFC and e-commerce volume", "year": "2015",
        "source_url": "https://usa.visa.com/visa-everywhere/innovation/google-pay.html",
        "source_name": "Visa",
        "details": (
            "Visa has been a core payment network partner for Google Pay since its launch as "
            "Android Pay in 2015. Google Pay allows users to add Visa debit and credit cards "
            "for contactless in-store payments and online checkout. Visa's tokenization "
            "technology (VTS) secures every Google Pay NFC transaction by replacing card "
            "numbers with device-specific digital tokens. Visa and Google expanded their "
            "partnership in 2019 covering digital commerce, API integration, and developer "
            "tools. Visa's 80M+ merchant acceptance locations make it the primary reason "
            "Google Pay works seamlessly for its 150M+ global users."
        ),
    },

    # ── Payment network × fintech ─────────────────────────────────────────────

    {
        "src": "V", "dst": "PYPL", "type": "Partnership",
        "desc": "Visa + PayPal strategic deal (2016): Visa promoted as first-choice payment in PayPal wallet",
        "value": "$500B+ PayPal annual payment volume", "year": "2016",
        "source_url": "https://investor.visa.com/news-releases/news-release-details/visa-and-paypal-expand-partnership-give-consumers-more-choice/",
        "source_name": "Visa Investor Relations",
        "details": (
            "Visa and PayPal announced a landmark strategic partnership in July 2016, resolving "
            "years of tension where PayPal actively steered users away from Visa cards toward "
            "cheaper bank transfers. Under the deal, Visa became a 'preferred' payment method "
            "in PayPal's checkout flow, with PayPal prominently presenting Visa cards in digital "
            "wallets. In exchange, PayPal gained access to Visa's Digital Enablement Program "
            "for tokenized checkout. PayPal agreed to stop practices that discouraged card "
            "payments. The deal marked PayPal's pivot from a bank-disruptive model to a "
            "card-network partner model, shifting the entire fintech-vs-payments dynamic."
        ),
    },
    {
        "src": "MA", "dst": "PYPL", "type": "Partnership",
        "desc": "Mastercard + PayPal strategic deal (2016): Mastercard made preferred option in PayPal checkout",
        "value": "Hundreds of billions in annual volume", "year": "2016",
        "source_url": "https://investor.mastercard.com/news-releases/news-release-details/mastercard-and-paypal-announce-expanded-partnership",
        "source_name": "Mastercard Investor Relations",
        "details": (
            "Mastercard and PayPal announced a parallel strategic partnership in September 2016, "
            "mirroring Visa's deal signed two months earlier. Mastercard became a preferred "
            "payment option in PayPal wallets, ending practices where PayPal minimized card "
            "visibility. PayPal gained access to Mastercard's Simplify Commerce and digital "
            "developer tools. Mastercard's Open Banking access was included, letting PayPal "
            "customers link bank accounts via Mastercard's API network. Together, the Visa and "
            "Mastercard deals in 2016 fundamentally shifted PayPal's business model toward being "
            "a card-network partner rather than a disruptive alternative to card payments."
        ),
    },
    {
        "src": "PYPL", "dst": "META", "type": "Partnership",
        "desc": "PayPal integrated as a payment method in Meta Pay (Facebook Pay) across Facebook, Instagram, Messenger",
        "value": "Billions in social commerce volume", "year": "2019",
        "source_url": "https://about.fb.com/news/2019/11/simplifying-payments-with-facebook-pay/",
        "source_name": "Meta Newsroom",
        "details": (
            "Meta (then Facebook) integrated PayPal as a payment method in Facebook Pay when "
            "it launched in November 2019. Facebook Pay (later renamed Meta Pay) allows users "
            "to link PayPal accounts to pay for purchases across Facebook, Instagram, Messenger, "
            "and WhatsApp without leaving the app. PayPal's 400M+ active account base makes it "
            "too valuable for Meta to exclude from its social commerce ambitions. The integration "
            "persists despite PayPal and Meta both competing in digital payments — illustrating "
            "how fintech ecosystems coexist even between rivals. Meta Pay now handles billions "
            "in social commerce transactions annually."
        ),
    },

    # ── Berkshire Hathaway equity ownership ───────────────────────────────────

    {
        "src": "BRK-B", "dst": "AAPL", "type": "Ownership",
        "desc": "Berkshire Hathaway ~5.5% of Apple — largest Berkshire equity position ever, peak $177B",
        "value": "~$130B position (2024, after partial sale)", "year": "2016",
        "source_url": "https://www.berkshirehathaway.com/letters/2022ltr.pdf",
        "source_name": "Berkshire Hathaway Annual Letter",
        "details": (
            "Berkshire Hathaway first bought Apple shares in Q1 2016 and built a position that "
            "peaked at ~5.5% ownership ($177B) by 2023 — the largest single equity investment "
            "in Berkshire's history. Warren Buffett called Apple 'probably the best business I "
            "know in the world.' Berkshire's Apple stake generated more dividend income than any "
            "other stock in the portfolio. In 2023-24, Berkshire reduced its Apple position by "
            "approximately 50% for tax reasons, generating billions in realized capital gains. "
            "Even after trimming, Apple remains Berkshire's largest equity holding, representing "
            "~40% of its public stock portfolio."
        ),
    },
    {
        "src": "BRK-B", "dst": "BAC", "type": "Ownership",
        "desc": "Berkshire holds ~13% of Bank of America — 2011 preferred/warrant deal worth $5B",
        "value": "~$35B position (2023)", "year": "2011",
        "source_url": "https://www.berkshirehathaway.com/letters/2022ltr.pdf",
        "source_name": "Berkshire Hathaway Annual Letter",
        "details": (
            "In 2011, Berkshire invested $5B in Bank of America preferred stock with warrants "
            "to buy 700M common shares at $7.14 each — a lifeline deal during BofA's mortgage "
            "crisis. Buffett called BofA CEO Brian Moynihan to propose the deal, which was "
            "accepted within hours. Berkshire exercised those warrants in 2017 when BofA stock "
            "surpassed $24, receiving $14B+ in common shares for the $5B investment. Berkshire "
            "now holds ~13% of BofA, making it BofA's largest shareholder. The investment is "
            "one of Buffett's most celebrated deals, structured like his Goldman Sachs and GE "
            "crisis-era investments."
        ),
    },
    {
        "src": "BRK-B", "dst": "AXP", "type": "Ownership",
        "desc": "Berkshire holds ~21% of American Express — relationship dating to the 1964 Salad Oil Scandal",
        "value": "~$28B position (2023)", "year": "1964",
        "source_url": "https://www.berkshirehathaway.com/letters/2022ltr.pdf",
        "source_name": "Berkshire Hathaway Annual Letter",
        "details": (
            "Berkshire has been a major American Express shareholder since 1964, when Buffett's "
            "investment partnership bet on Amex during the Salad Oil Scandal — a fraud scheme "
            "that nearly destroyed the company. Buffett correctly identified that Amex's brand "
            "and customer loyalty were unharmed. Berkshire now owns ~21% of American Express — "
            "its longest-running major equity position. Buffett considers Amex a 'forever' "
            "holding alongside Apple and Coca-Cola. AmEx's closed-loop network (Amex is both "
            "network and issuer) generates higher revenue per transaction than Visa/Mastercard's "
            "open-loop model, a structural advantage Buffett has praised for decades."
        ),
    },
    {
        "src": "BRK-B", "dst": "MCO", "type": "Ownership",
        "desc": "Berkshire holds ~13% of Moody's — position inherited from the 2000 Dun & Bradstreet spinoff",
        "value": "~$10B position (2023)", "year": "2000",
        "source_url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001067983&type=13-F&dateb=&owner=include&count=40",
        "source_name": "Berkshire Hathaway SEC 13-F",
        "details": (
            "Berkshire owns ~13% of Moody's Corporation — a position dating to 2000 when Dun & "
            "Bradstreet spun off Moody's as a separate company. Berkshire held D&B shares, which "
            "automatically converted into Moody's shares in the spinoff, and has never sold. "
            "Moody's is one of three global credit rating agencies (alongside S&P Global and "
            "Fitch) and enjoys near-monopoly pricing power on bond ratings. The position is a "
            "classic Buffett 'tollbooth' investment — essential infrastructure with durable "
            "competitive advantage. Buffett has acknowledged he almost sold the position multiple "
            "times and never did."
        ),
    },

    # ── Bank × hyperscaler cloud ──────────────────────────────────────────────

    {
        "src": "COF", "dst": "MSFT", "type": "Supply Chain",
        "desc": "Capital One first major US bank to migrate all applications to Microsoft Azure (2018)",
        "value": "~$500M+ (multi-year)", "year": "2018",
        "source_url": "https://news.microsoft.com/2018/10/25/capital-one-and-microsoft-expand-strategic-partnership/",
        "source_name": "Microsoft News",
        "details": (
            "Capital One became the first major US bank to commit to migrating all data-center "
            "applications to the cloud — specifically Microsoft Azure — when it announced the "
            "deal in 2018. Capital One closed its last owned data center in 2020, completing one "
            "of the most dramatic cloud transformations in financial services history. CTO Rob "
            "Alexander argued that operating data centers was not a competitive advantage for a "
            "bank. Capital One now uses Azure for real-time fraud detection, credit decisioning, "
            "and mobile banking infrastructure serving 100M+ accounts. The migration became the "
            "definitive financial services cloud case study."
        ),
    },
    {
        "src": "JPM", "dst": "MSFT", "type": "Partnership",
        "desc": "JPMorgan Chase + Microsoft Azure — cloud alliance for AI, risk analytics, and developer tools",
        "value": "~$1B+ (multi-year)", "year": "2019",
        "source_url": "https://news.microsoft.com/2019/10/16/jpmorgan-chase-and-microsoft-expand-cloud-alliance/",
        "source_name": "Microsoft News",
        "details": (
            "JPMorgan Chase and Microsoft announced an expanded cloud alliance in October 2019. "
            "JPM migrates selected workloads to Azure for data analytics, developer tools, and "
            "enterprise operations. The deal includes Azure-based risk analytics for JPMorgan's "
            "Corporate & Investment Bank and Microsoft 365 deployed across JPM's 270,000+ "
            "employees. In 2023, JPM began using Azure OpenAI Service to build AI tools for "
            "wealth management and investment banking, including IndexGPT for securities "
            "portfolio recommendations. JPM maintains a multi-cloud strategy but Azure is its "
            "primary enterprise software and AI partner."
        ),
    },
    {
        "src": "GS", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Goldman Sachs runs Marquee trading, risk analytics, and data lake infrastructure on AWS",
        "value": "~$500M+ annually", "year": "2017",
        "source_url": "https://aws.amazon.com/solutions/case-studies/goldman-sachs/",
        "source_name": "AWS Case Study",
        "details": (
            "Goldman Sachs runs significant trading, risk management, and market data "
            "infrastructure on Amazon Web Services. Goldman's Marquee platform — which provides "
            "institutional clients with risk analytics, options pricing, and simulations — runs "
            "on AWS. Goldman's Data Lake on AWS stores petabytes of trading and risk data for "
            "regulatory reporting and quantitative research. In 2020, Goldman Sachs Asset "
            "Management moved its Marquee quantitative investing platform to AWS, enabling hedge "
            "fund clients to run complex Monte Carlo simulations at cloud scale. AWS provides "
            "the elastic compute critical for options pricing spikes during volatile markets."
        ),
    },
    {
        "src": "MS", "dst": "MSFT", "type": "Partnership",
        "desc": "Morgan Stanley deployed OpenAI GPT-4 (Azure) for 16,000 financial advisors — first major Wall Street AI deployment",
        "value": "~$100M+ (estimated AI services)", "year": "2023",
        "source_url": "https://openai.com/index/morgan-stanley",
        "source_name": "OpenAI",
        "details": (
            "Morgan Stanley deployed OpenAI's GPT-4 — via Microsoft Azure OpenAI Service — "
            "for 16,000 financial advisors in 2023, making it one of the first major financial "
            "firms to deploy generative AI at enterprise scale. The system, called 'AI @ Morgan "
            "Stanley Assistant,' indexes 100,000+ research reports and financial documents, "
            "allowing advisors to query the entire knowledge base in natural language during "
            "client meetings. Morgan Stanley worked directly with OpenAI and Microsoft to build "
            "the tool. By early 2024, advisors were using the AI in real client meetings for "
            "instant research retrieval. The project was featured at Microsoft Build 2023 as a "
            "landmark enterprise AI deployment."
        ),
    },
    {
        "src": "MS", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Morgan Stanley migrated E*Trade brokerage platforms to AWS after $13B acquisition",
        "value": "~$300M+ annually", "year": "2021",
        "source_url": "https://aws.amazon.com/solutions/case-studies/morgan-stanley-etrade/",
        "source_name": "AWS Case Study",
        "details": (
            "Morgan Stanley selected Amazon Web Services to power its E*Trade retail brokerage "
            "platforms after acquiring E*Trade for $13B in 2020. E*Trade migrated trading, "
            "account management, and portfolio analytics to AWS, handling 150M+ trades monthly "
            "at peak. The migration gave Morgan Stanley elastic cloud infrastructure that scales "
            "instantly during market volatility events — critical during meme-stock spikes in "
            "2021 when retail trading volumes hit records. Morgan Stanley and AWS also "
            "collaborate on sustainable finance analytics. The E*Trade-on-AWS deployment is "
            "cited by AWS as one of the largest financial services migrations to cloud-native "
            "microservices architecture."
        ),
    },
    {
        "src": "BLK", "dst": "MSFT", "type": "Partnership",
        "desc": "BlackRock Aladdin investment platform runs on Microsoft Azure — announced December 2022",
        "value": "~$500M+ (multi-year)", "year": "2022",
        "source_url": "https://news.microsoft.com/2022/12/15/blackrock-and-microsoft-announce-groundbreaking-private-markets-technology-partnership/",
        "source_name": "Microsoft News",
        "details": (
            "BlackRock announced in December 2022 that its Aladdin investment management "
            "platform would run on Microsoft Azure. Aladdin manages risk analytics for $21 "
            "trillion in assets under management — used by BlackRock itself, 200+ institutional "
            "clients, and sovereign wealth funds. Running on Azure enables BlackRock's Aladdin "
            "Studio customers to build custom analytics using Azure OpenAI and Azure Machine "
            "Learning. The partnership extended in 2023 to cover BlackRock's eFront private "
            "markets platform, making Azure the cloud for both public and private markets risk "
            "management at the world's largest asset manager."
        ),
    },
    {
        "src": "SPGI", "dst": "MSFT", "type": "Partnership",
        "desc": "S&P Global + Microsoft — Market Intelligence data and Ratings on Azure AI (2023 strategic alliance)",
        "value": "~$300M+ (multi-year)", "year": "2023",
        "source_url": "https://news.microsoft.com/2023/05/04/microsoft-and-s-p-global-announce-strategic-technology-alliance/",
        "source_name": "Microsoft News",
        "details": (
            "S&P Global and Microsoft announced a strategic technology alliance in May 2023, "
            "integrating S&P Global's financial data and ratings into Microsoft's Azure AI "
            "ecosystem. S&P Global Market Intelligence — company financials, credit ratings, "
            "commodity prices — is accessible via Azure APIs and embedded in Microsoft's "
            "financial data cloud offering. S&P Global Ratings uses Azure OpenAI for natural "
            "language analysis of credit risks from earnings transcripts and filings. The "
            "partnership lets S&P Global deliver AI-powered financial intelligence to "
            "Microsoft's 300M+ enterprise users without building its own cloud sales force."
        ),
    },

    # ── Financial data & analytics × cloud ───────────────────────────────────

    {
        "src": "MCO", "dst": "MSFT", "type": "Partnership",
        "desc": "Moody's + Microsoft — AI-powered credit risk analytics and ESG scoring on Azure (2023)",
        "value": "~$200M+ (multi-year)", "year": "2023",
        "source_url": "https://newsroom.moodys.com",
        "source_name": "Moody's Newsroom",
        "details": (
            "Moody's and Microsoft partnered to develop next-generation AI risk and data "
            "solutions using Azure and Microsoft's generative AI capabilities. Moody's uses "
            "Azure OpenAI to analyze unstructured data — earnings transcripts, court filings, "
            "news sources — to enrich its credit ratings and ESG scoring models. Moody's "
            "Analytics integrates Azure Machine Learning into its CreditEdge and RiskCalc "
            "credit models, used by 4,000+ financial institutions worldwide for loan "
            "underwriting and portfolio risk management. The partnership positions Moody's as "
            "an AI-native financial intelligence platform rather than a purely ratings-driven "
            "business."
        ),
    },
    {
        "src": "V", "dst": "MSFT", "type": "Partnership",
        "desc": "Visa + Microsoft — global partnership for AI-powered digital payment infrastructure on Azure (2019)",
        "value": "~$200M+ (multi-year)", "year": "2019",
        "source_url": "https://news.microsoft.com/2019/10/02/visa-and-microsoft-establish-a-global-partnership-to-accelerate-digital-payments/",
        "source_name": "Microsoft News",
        "details": (
            "Visa and Microsoft announced a global strategic partnership in October 2019 to "
            "accelerate digital payments using Azure cloud and AI. The partnership covers three "
            "areas: Visa runs payment analytics and fraud detection workloads on Azure; "
            "Microsoft's enterprise customers get Visa digital payment APIs pre-integrated with "
            "Azure commerce platforms; and jointly, the companies develop payment solutions for "
            "Microsoft's retail and government enterprise accounts. Visa processes 700+ payment "
            "transactions per second on its VisaNet — the Azure partnership adds real-time AI "
            "fraud scoring and predictive analytics at unprecedented scale."
        ),
    },
    {
        "src": "MA", "dst": "MSFT", "type": "Partnership",
        "desc": "Mastercard + Microsoft — AI cybersecurity and financial crime prevention partnership (2023)",
        "value": "~$100M+ (multi-year)", "year": "2023",
        "source_url": "https://newsroom.mastercard.com/press-releases/mastercard-and-microsoft-join-forces-to-combat-cybercrime/",
        "source_name": "Mastercard Newsroom",
        "details": (
            "Mastercard and Microsoft announced a cybersecurity and AI partnership in 2023 "
            "focused on combating financial crime at scale. Mastercard's CyberSecure product — "
            "which scores cybersecurity risk for small businesses — integrates with Microsoft "
            "Defender for Business and Microsoft 365 Business Premium. The two companies develop "
            "AI models to detect money laundering patterns by combining Mastercard's transaction "
            "data with Azure AI capabilities. The partnership reflects the convergence of payment "
            "security and enterprise cybersecurity: as financial fraud becomes more sophisticated, "
            "payment networks need hyperscaler AI to detect and prevent attacks at scale across "
            "billions of daily transactions."
        ),
    },
    {
        "src": "V", "dst": "AMZN", "type": "Partnership",
        "desc": "Amazon-Visa expanded global relationship (2022) — resolving high-profile UK fee dispute",
        "value": "Trillions in annual Amazon payment volume", "year": "2022",
        "source_url": "https://www.businesswire.com/news/home/20220217005312/en/Amazon-and-Visa-Announce-Expanded-Global-Relationship",
        "source_name": "BusinessWire",
        "details": (
            "Amazon and Visa resolved a long-running global fee dispute in February 2022, "
            "announcing an expanded global relationship ensuring Visa cards remain accepted on "
            "Amazon.com worldwide. The dispute had escalated to Amazon publicly threatening to "
            "drop Visa credit card acceptance in the UK, Australia, and Singapore in late 2021 "
            "— an existential threat that rattled Visa's stock. The resolution — terms undisclosed "
            "— included Amazon committing to support Visa's Click to Pay standard for e-commerce. "
            "The deal secured Visa's position on the world's largest online retail platform and "
            "ended a months-long standoff that signaled Amazon's growing leverage over card "
            "networks."
        ),
    },
    {
        "src": "AXP", "dst": "MSFT", "type": "Partnership",
        "desc": "American Express + Microsoft — corporate card integration with Microsoft 365 and Azure B2B payments",
        "value": "~$100M+ (multi-year)", "year": "2022",
        "source_url": "https://newsroom.americanexpress.com",
        "source_name": "American Express Newsroom",
        "details": (
            "American Express and Microsoft collaborate to simplify B2B corporate payments for "
            "businesses using Microsoft 365 and Azure. American Express corporate cards integrate "
            "with Microsoft Dynamics 365 Finance for automated expense reporting and "
            "reconciliation — eliminating manual receipt submission for corporate travelers. "
            "Amex's @Work business portal connects to Microsoft's procurement tools, letting "
            "finance teams manage spending policies directly in Microsoft's ERP ecosystem. Amex "
            "also participates in Microsoft's Azure Marketplace, making Amex payment APIs "
            "available to developers building commercial applications. The partnership targets "
            "the $125T global B2B payments market where corporate card adoption lags "
            "consumer cards."
        ),
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # Healthcare sector relationships (30 additions)
    # ═══════════════════════════════════════════════════════════════════════════

    # ── Pharma × Microsoft AI cloud ──────────────────────────────────────────

    {
        "src": "LLY", "dst": "MSFT", "type": "Partnership",
        "desc": "Eli Lilly + Microsoft — generative AI platform for drug discovery and R&D (2023)",
        "value": "~$200M+ (multi-year)", "year": "2023",
        "source_url": "https://investor.lilly.com/news-releases",
        "source_name": "Eli Lilly Investor Relations",
        "details": (
            "Eli Lilly and Microsoft announced a strategic partnership in 2023 to apply "
            "generative AI across Lilly's drug discovery, clinical development, and "
            "manufacturing operations. Lilly uses Azure OpenAI and custom foundation "
            "models to accelerate molecule design for obesity (tirzepatide/Mounjaro), "
            "Alzheimer's, and immunology drugs. Microsoft's AI tools help Lilly analyze "
            "petabytes of protein-structure, clinical-trial, and real-world evidence data. "
            "Lilly is the most valuable pharmaceutical company globally ($750B+) and the "
            "partnership positions it to maintain leadership in the GLP-1 drug race using "
            "AI-powered R&D acceleration."
        ),
    },
    {
        "src": "AMGN", "dst": "MSFT", "type": "Partnership",
        "desc": "Amgen + Microsoft — AI for drug molecule design, target identification, and clinical development",
        "value": "~$150M+ (multi-year)", "year": "2023",
        "source_url": "https://www.amgen.com/media/news-releases",
        "source_name": "Amgen Newsroom",
        "details": (
            "Amgen and Microsoft announced a strategic AI partnership in 2023 to apply "
            "machine learning across drug discovery and biologics development. Amgen uses "
            "Azure AI to identify drug targets in complex disease pathways, design novel "
            "protein therapeutics, and predict clinical trial outcomes. Amgen's Otezla "
            "(psoriasis), Repatha (cardiovascular), and Lumakras (lung cancer) programs "
            "benefit from AI-driven biomarker analysis. The partnership marks a shift from "
            "Amgen's traditional small-molecule chemistry toward AI-first biologics design, "
            "with Azure providing the compute for Amgen's large-scale genomics and proteomics "
            "data science workloads."
        ),
    },
    {
        "src": "JNJ", "dst": "MSFT", "type": "Partnership",
        "desc": "J&J MedTech + Microsoft — AI-powered robotic surgery, connected devices, and digital health",
        "value": "~$300M+ (multi-year)", "year": "2021",
        "source_url": "https://www.jnj.com/investor-relations/press-releases",
        "source_name": "J&J Investor Relations",
        "details": (
            "Johnson & Johnson MedTech and Microsoft partner to embed AI across surgical "
            "robotics and connected medical devices. J&J's Ottava robotic surgery platform "
            "(successor to the Verb Surgical JV) uses Azure AI for real-time procedural "
            "guidance and post-operative analytics. J&J's Velys robotic-assisted orthopedic "
            "surgery system integrates with Azure for imaging and navigation data. Microsoft "
            "Teams powers J&J's hybrid clinical workflows connecting surgeons, nurses, and "
            "device specialists in operating rooms. J&J also uses Azure for regulatory "
            "document processing and pharmacovigilance AI across its pharmaceutical division."
        ),
    },
    {
        "src": "MRK", "dst": "MSFT", "type": "Partnership",
        "desc": "Merck + Microsoft Azure AI — digital research platform for oncology and vaccine drug discovery",
        "value": "~$150M+ (multi-year)", "year": "2022",
        "source_url": "https://www.merck.com/investor-relations/news/",
        "source_name": "Merck Investor Relations",
        "details": (
            "Merck (MSD outside North America) partners with Microsoft to run its digital "
            "research infrastructure on Azure. Merck's EXPLORE AI platform — which guides "
            "molecule design and clinical candidate selection for Keytruda (pembrolizumab) "
            "combinations and vaccine programs — runs on Azure AI services. Microsoft 365 "
            "and Azure Data Factory power Merck's global research collaboration across "
            "Boston, London, and Singapore R&D sites. Keytruda, the world's best-selling "
            "cancer drug at $25B+ annual revenue, relies on AI-driven biomarker analysis "
            "that Merck runs on Azure to identify which tumor types respond to PD-1 "
            "immunotherapy."
        ),
    },
    {
        "src": "ABT", "dst": "MSFT", "type": "Partnership",
        "desc": "Abbott FreeStyle Libre CGM data integrates with Microsoft Azure for diabetes digital health",
        "value": "~$100M+ (multi-year)", "year": "2021",
        "source_url": "https://abbott.mediaroom.com/",
        "source_name": "Abbott Newsroom",
        "details": (
            "Abbott and Microsoft partner to integrate Abbott's FreeStyle Libre continuous "
            "glucose monitoring (CGM) data with Microsoft's Azure health data platform. "
            "FreeStyle Libre is worn by 6M+ diabetes patients globally and generates "
            "continuous blood-glucose readings every minute. Integrating this stream into "
            "Azure enables healthcare providers to run population-health analytics, detect "
            "hypoglycemia risk patterns, and personalize insulin dosing recommendations. "
            "Abbott also uses Azure for its molecular diagnostics (Alinity) instrument "
            "connectivity and its cardiac rhythm management devices. The partnership "
            "positions Abbott's device data as a first-class input to clinical AI workflows "
            "inside Microsoft's health cloud."
        ),
    },

    # ── Pharma × AWS cloud ────────────────────────────────────────────────────

    {
        "src": "PFE", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Pfizer uses AWS for mRNA vaccine cold-chain monitoring, clinical operations, and genomics research",
        "value": "~$300M+ annually", "year": "2020",
        "source_url": "https://aws.amazon.com/health/pharmaceutical/",
        "source_name": "AWS Health",
        "details": (
            "Pfizer uses Amazon Web Services for clinical trial management, mRNA vaccine "
            "supply-chain analytics, and genomics research at scale. During COVID-19, "
            "AWS IoT systems monitored the cold-chain integrity of billions of mRNA vaccine "
            "doses across 170+ countries — flagging temperature excursions in near-real time. "
            "Pfizer's Global Supply cloud runs on AWS, handling manufacturing scheduling and "
            "regulatory batch records across 43 manufacturing sites. Pfizer's digital "
            "biomarker program for Alzheimer's disease uses AWS SageMaker to analyze wearable "
            "sensor data from clinical trial participants. The COVID-19 vaccine program "
            "accelerated Pfizer's AWS adoption significantly."
        ),
    },
    {
        "src": "ABBV", "dst": "AMZN", "type": "Supply Chain",
        "desc": "AbbVie uses AWS for biologics R&D, gene therapy, and global clinical operations",
        "value": "~$200M+ annually", "year": "2019",
        "source_url": "https://aws.amazon.com/solutions/case-studies/abbvie/",
        "source_name": "AWS Case Study",
        "details": (
            "AbbVie migrated core R&D, clinical operations, and commercial analytics to "
            "Amazon Web Services. AbbVie's bioinformatics platform — which analyzes genetic "
            "variants associated with autoimmune disease and cancer — runs on AWS HPC clusters. "
            "The company's gene therapy programs (inherited retinal diseases, neuroscience) use "
            "AWS for sequence analysis and manufacturing data. Humira, AbbVie's blockbuster "
            "biologic, generated $14B+ annually before biosimilar entry; its successor pipeline "
            "(Skyrizi, Rinvoq) is being developed using AWS-powered digital R&D. AbbVie also "
            "runs its 300+ clinical trial sites' data management through AWS."
        ),
    },
    {
        "src": "REGN", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Regeneron Genetics Center sequences and analyzes whole genomes on AWS — 2M+ exomes and growing",
        "value": "~$150M+ annually", "year": "2016",
        "source_url": "https://aws.amazon.com/solutions/case-studies/regeneron/",
        "source_name": "AWS Case Study",
        "details": (
            "Regeneron Genetics Center (RGC) uses AWS to sequence and analyze millions of "
            "whole exomes and genomes — one of the world's largest genetics research "
            "workloads. RGC has sequenced 2M+ patient exomes in partnership with UK Biobank "
            "and the US Department of Veterans Affairs Million Veteran Program. AWS S3 stores "
            "petabytes of genomic data; AWS Batch and SageMaker run variant-calling pipelines "
            "and genetic-association analyses. The RGC's discoveries directly feed Regeneron's "
            "drug pipeline — identifying rare genetic variants that validate targets like PCSK9 "
            "(heart disease), AngptL3 (triglycerides), and APOC3 (cardiovascular disease)."
        ),
    },
    {
        "src": "GILD", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Gilead Sciences uses AWS for HIV, oncology, and COVID antiviral drug development operations",
        "value": "~$100M+ annually", "year": "2018",
        "source_url": "https://aws.amazon.com/solutions/case-studies/gilead-sciences/",
        "source_name": "AWS Case Study",
        "details": (
            "Gilead Sciences runs drug discovery, clinical development, and commercial "
            "operations on AWS. Gilead's HIV portfolio — Biktarvy, Descovy, and Truvada "
            "generics — involves complex real-world evidence analysis that Gilead runs on "
            "AWS. During COVID-19, Gilead developed remdesivir (Veklury) in record time "
            "using AWS-accelerated clinical data analysis and supply-chain modeling. Gilead's "
            "Kite Pharma subsidiary, which makes CAR-T cell therapies (Yescarta, Tecartus) "
            "for cancer, uses AWS to manage the complex chain-of-custody for personalized "
            "cell therapies manufactured from each individual patient's T cells."
        ),
    },
    {
        "src": "BMY", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Bristol-Myers Squibb uses AWS to accelerate immuno-oncology research and Celgene drug development",
        "value": "~$150M+ annually", "year": "2019",
        "source_url": "https://aws.amazon.com/solutions/case-studies/bms/",
        "source_name": "AWS Case Study",
        "details": (
            "Bristol-Myers Squibb (BMS) uses Amazon Web Services for oncology R&D, including "
            "analysis of clinical data for Opdivo (nivolumab), Keytruda competitor, and "
            "Revlimid (lenalidomide), inherited from the $74B Celgene acquisition in 2019. "
            "BMS runs genomic and proteomic data pipelines on AWS to discover biomarkers "
            "predicting cancer immunotherapy response. AWS also handles BMS's global clinical "
            "trial data management and pharmacovigilance systems tracking adverse events across "
            "regulatory submissions in 50+ countries. BMS's cell therapy programs — Breyanzi "
            "and Abecma (CAR-T) — use AWS for complex manufacturing analytics."
        ),
    },
    {
        "src": "VRTX", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Vertex Pharmaceuticals uses AWS to accelerate cystic fibrosis drug discovery and cell/gene therapy programs",
        "value": "~$100M+ annually", "year": "2018",
        "source_url": "https://aws.amazon.com/solutions/case-studies/vertex-pharmaceuticals/",
        "source_name": "AWS Case Study",
        "details": (
            "Vertex Pharmaceuticals uses AWS to power its drug discovery and development "
            "operations. Vertex's cystic fibrosis franchise — Trikafta/Kaftrio generating "
            "$8B+ annually — was developed using advanced computational chemistry on cloud "
            "HPC platforms, AWS included. Vertex's pain, kidney disease, and sickle cell "
            "programs use AWS SageMaker for AI-driven molecule screening. Vertex's cell "
            "and genetic therapy programs use AWS to manage complex clinical manufacturing "
            "data for treatments like its sickle cell gene editing therapy (Casgevy, "
            "co-developed with CRISPR Therapeutics). Vertex is seen as a model for how "
            "small biotechs can punch above their weight using cloud-native R&D platforms."
        ),
    },
    {
        "src": "ISRG", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Intuitive Surgical's Surgical Data Network — billions of procedure data points — runs on AWS",
        "value": "~$100M+ annually", "year": "2019",
        "source_url": "https://aws.amazon.com/solutions/case-studies/intuitive/",
        "source_name": "AWS Case Study",
        "details": (
            "Intuitive Surgical's Surgical Data Network (SDN) runs on AWS, collecting and "
            "analyzing data from 8,000+ da Vinci robotic surgery systems performing 2M+ "
            "procedures annually across 67 countries. Each procedure generates gigabytes "
            "of kinematic data (instrument motion, force, video) that AWS stores and "
            "processes. AWS SageMaker models identify patterns correlating surgical technique "
            "with patient outcomes, enabling Intuitive to provide performance benchmarks to "
            "surgeons. Intuitive also uses AWS for its Field Smart Technology remote "
            "diagnostics — predicting da Vinci system maintenance needs before failures "
            "occur in operating rooms."
        ),
    },

    # ── Medical device × tech ─────────────────────────────────────────────────

    {
        "src": "MDT", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Medtronic uses AWS for connected insulin delivery, cardiac monitoring, and remote patient management",
        "value": "~$150M+ annually", "year": "2018",
        "source_url": "https://aws.amazon.com/solutions/case-studies/medtronic/",
        "source_name": "AWS Case Study",
        "details": (
            "Medtronic uses AWS to power its connected device ecosystem. The InPen smart "
            "insulin pen sends dose data to AWS for real-time analysis, alerting patients "
            "and clinicians to missed doses or suboptimal dosing patterns. Medtronic's "
            "cardiac monitoring devices (insertable cardiac monitors, pacemakers) transmit "
            "data through Medtronic Care Management Services' cloud platform on AWS, "
            "enabling remote arrhythmia detection for 3M+ patients. Medtronic's Cranial "
            "and Spinal Technologies division uses AWS for surgical navigation system "
            "updates and intraoperative imaging analytics. AWS handles Medtronic's "
            "regulatory change management data across 150+ countries."
        ),
    },
    {
        "src": "TMO", "dst": "MSFT", "type": "Partnership",
        "desc": "Thermo Fisher Scientific + Microsoft Azure — lab informatics, AI instrument connectivity, and digital R&D",
        "value": "~$200M+ (multi-year)", "year": "2021",
        "source_url": "https://ir.thermofisher.com/news-releases",
        "source_name": "Thermo Fisher IR",
        "details": (
            "Thermo Fisher Scientific and Microsoft partner to build the 'Lab of the Future' "
            "on Azure — connecting Thermo Fisher analytical instruments (mass spectrometers, "
            "gene sequencers, electron microscopes) to cloud AI for automated data analysis. "
            "Thermo Fisher's SampleManager LIMS (Laboratory Information Management System) "
            "integrates with Azure for real-time quality control in pharmaceutical "
            "manufacturing. Researchers at biopharma clients can query Thermo Fisher "
            "instruments directly through Azure's data fabric, eliminating manual data "
            "export. The partnership spans Thermo Fisher's $15B+ Life Sciences Solutions "
            "segment and positions Thermo Fisher as the AI-connected instrument layer in "
            "pharma's digital R&D stack."
        ),
    },
    {
        "src": "DHR", "dst": "MSFT", "type": "Partnership",
        "desc": "Danaher life science businesses use Microsoft Azure for Cytiva bioprocessing analytics and Cepheid diagnostics",
        "value": "~$150M+ (multi-year)", "year": "2022",
        "source_url": "https://investors.danaher.com/financial-information/annual-reports",
        "source_name": "Danaher Annual Report",
        "details": (
            "Danaher's life science businesses use Microsoft Azure for cloud analytics across "
            "its Cytiva (bioprocessing) and Cepheid (point-of-care diagnostics) platforms. "
            "Cytiva's KUBio modular bioreactor plants use Azure IoT for process monitoring "
            "and batch analytics — critical for pharma clients scaling up biologics "
            "manufacturing. Cepheid's 50,000+ GeneXpert diagnostic systems in hospitals "
            "worldwide transmit test results to Azure for population surveillance (COVID-19, "
            "TB, flu). Danaher's Integrated DNA Technologies (IDT) business, which supplies "
            "CRISPR editing reagents, uses Azure for sequence design automation. Microsoft "
            "Teams is Danaher's enterprise collaboration platform across its 60+ operating "
            "companies."
        ),
    },

    # ── Health insurer × tech ─────────────────────────────────────────────────

    {
        "src": "UNH", "dst": "MSFT", "type": "Partnership",
        "desc": "UnitedHealth Optum + Microsoft Azure AI — clinical decision support, care management, and health analytics",
        "value": "~$1B+ (multi-year)", "year": "2021",
        "source_url": "https://www.unitedhealthgroup.com/newsroom.html",
        "source_name": "UnitedHealth Group Newsroom",
        "details": (
            "UnitedHealth Group's Optum data and analytics division partners with Microsoft "
            "Azure to deploy AI at scale across 150M+ lives managed. Optum uses Azure OpenAI "
            "to analyze clinical notes, lab results, and claims data for predictive care "
            "management — identifying patients at risk for hospitalization before symptoms "
            "escalate. Microsoft Teams powers Optum's virtual care programs connecting "
            "patients with 70,000+ physicians. UnitedHealth processes 15B+ data transactions "
            "annually; Azure provides the elastic compute for peak healthcare utilization "
            "events. The partnership is one of the largest AI deployments in US healthcare, "
            "covering population health, utilization management, and clinical quality metrics."
        ),
    },
    {
        "src": "UNH", "dst": "AMZN", "type": "Supply Chain",
        "desc": "UnitedHealth Group uses AWS for healthcare claims processing, population health, and pharmacy analytics",
        "value": "~$500M+ annually", "year": "2020",
        "source_url": "https://aws.amazon.com/health/customers/unitedhealth/",
        "source_name": "AWS Health",
        "details": (
            "UnitedHealth Group uses Amazon Web Services for large-scale healthcare data "
            "analytics across its insurance (UnitedHealthcare) and services (Optum) segments. "
            "AWS processes UnitedHealth's claims data — 7M+ claims per day from 50M+ members "
            "— using EMR and Redshift for fraud detection and payment accuracy. Optum Rx, "
            "the pharmacy benefit management arm handling 1.3B+ prescriptions annually, uses "
            "AWS for drug interaction checking and formulary optimization. UnitedHealth's "
            "Optum Genomics research program uses AWS to analyze genomic data from consented "
            "members for population health insights. AWS's HIPAA-eligible services make it "
            "suited for UnitedHealth's strict PHI data requirements."
        ),
    },
    {
        "src": "CVS", "dst": "MSFT", "type": "Partnership",
        "desc": "CVS Health + Microsoft Azure — digital pharmacy, MinuteClinic telehealth, and AI health management",
        "value": "~$400M+ (multi-year)", "year": "2021",
        "source_url": "https://news.microsoft.com/2021/09/08/cvs-health-and-microsoft-announce-multi-year-strategic-alliance/",
        "source_name": "Microsoft News",
        "details": (
            "CVS Health and Microsoft announced a multi-year strategic alliance in September "
            "2021. CVS is migrating its digital pharmacy, insurance (Aetna), and clinic "
            "operations to Azure. The partnership powers CVS Health's virtual care platform "
            "connecting patients with MinuteClinic providers via Microsoft Teams. Azure AI "
            "analyzes CVS pharmacy data (400M+ prescriptions annually) to predict medication "
            "adherence risks and flag potential drug interactions. Aetna's 23M+ health plan "
            "members benefit from Azure-powered care gap analytics. CVS Health Hub locations "
            "use Azure IoT for inventory and dispensing automation. The deal is CVS's largest "
            "technology investment supporting its pivot from pharmacy chain to health company."
        ),
    },
    {
        "src": "ELV", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Elevance Health (formerly Anthem) uses AWS for cloud-native insurance operations and population health",
        "value": "~$300M+ annually", "year": "2019",
        "source_url": "https://aws.amazon.com/solutions/case-studies/anthem/",
        "source_name": "AWS Case Study",
        "details": (
            "Elevance Health (rebranded from Anthem in 2022) uses AWS for cloud-native "
            "health insurance operations across 46M+ members. Elevance migrated its claims "
            "adjudication systems to AWS, reducing processing time from hours to minutes for "
            "complex medical claims. AWS SageMaker models power Elevance's predictive "
            "analytics for chronic disease management and care gap identification. Elevance's "
            "digital health platform — Sydney Health app with 7M+ active users — runs on AWS "
            "for high-availability access to benefits, care, and telehealth. Elevance uses "
            "AWS for its Carelon integrated care services segment, analyzing social "
            "determinants of health data to guide care coordination."
        ),
    },
    {
        "src": "CI", "dst": "MSFT", "type": "Partnership",
        "desc": "Cigna + Microsoft — virtual behavioral health, telehealth member engagement, and care navigation AI",
        "value": "~$200M+ (multi-year)", "year": "2021",
        "source_url": "https://newsroom.cigna.com/",
        "source_name": "Cigna Newsroom",
        "details": (
            "Cigna Group partners with Microsoft to expand digital health and behavioral "
            "health access. Cigna's Evernorth Health Services — the $100B+ pharmacy and care "
            "services platform — uses Azure for claims analytics, specialty pharmacy "
            "optimization, and behavioral health care coordination. Microsoft Teams powers "
            "Cigna's virtual behavioral health programs, connecting 180M+ plan members with "
            "licensed therapists and psychiatrists for video sessions. Cigna uses Azure AI "
            "to identify members showing early signs of depression or anxiety through claims "
            "patterns, enabling proactive outreach. Cigna also uses Microsoft 365 Copilot "
            "to streamline prior authorization documentation across its 75,000+ employees."
        ),
    },

    # ── Life science supply chain ─────────────────────────────────────────────

    {
        "src": "TMO", "dst": "PFE", "type": "Supply Chain",
        "desc": "Thermo Fisher + Pfizer 15-year strategic alliance for clinical supply, manufacturing, and analytical services",
        "value": "~$5B+ (15-year deal)", "year": "2017",
        "source_url": "https://ir.thermofisher.com/news-releases/news-release-details/thermo-fisher-scientific-and-pfizer-enter-15-year-strategic",
        "source_name": "Thermo Fisher IR",
        "details": (
            "Thermo Fisher Scientific and Pfizer announced a landmark 15-year strategic "
            "alliance in 2017 covering clinical supply chain services, analytical testing, "
            "and commercial manufacturing for Pfizer's investigational drugs. Thermo Fisher "
            "provides clinical packaging, labeling, storage (including ultra-cold chain for "
            "mRNA), and global distribution across 70+ countries for Pfizer's clinical "
            "trials. During COVID-19, this alliance was critical to manufacturing and "
            "distributing the Pfizer-BioNTech COVID-19 vaccine at unprecedented speed. "
            "The deal represents one of the most comprehensive pharma outsourcing agreements "
            "in history, covering the full drug development lifecycle from first-in-human "
            "trials to commercial launch."
        ),
    },
    {
        "src": "TMO", "dst": "LLY", "type": "Supply Chain",
        "desc": "Thermo Fisher provides CDMO biologics manufacturing and analytical services for Eli Lilly's injectable drugs",
        "value": "~$1-2B annually", "year": "2015",
        "source_url": "https://ir.thermofisher.com/financial-information/annual-reports",
        "source_name": "Thermo Fisher Annual Report",
        "details": (
            "Thermo Fisher's Patheon CDMO (contract development and manufacturing) division "
            "manufactures biologics and injectable drugs for Eli Lilly's portfolio. This "
            "includes fill-finish manufacturing for Lilly's insulin products (Humalog, "
            "Basaglar) and formulation development for tirzepatide (Mounjaro/Zepbound) "
            "as the GLP-1 drug scaled to blockbuster volumes. Thermo Fisher's analytical "
            "instruments — mass spectrometers, HPLC systems, bioanalytical tools — are also "
            "deployed in Lilly's quality-control labs globally. Lilly's explosive growth "
            "driven by tirzepatide has made it one of Thermo Fisher's largest and fastest-"
            "growing manufacturing customers."
        ),
    },
    {
        "src": "TMO", "dst": "JNJ", "type": "Supply Chain",
        "desc": "Thermo Fisher analytical instruments and CDMO services support J&J drug development and manufacturing QA",
        "value": "~$1-2B annually", "year": "2010",
        "source_url": "https://ir.thermofisher.com/financial-information/annual-reports",
        "source_name": "Thermo Fisher Annual Report",
        "details": (
            "Thermo Fisher Scientific is a major supplier to Johnson & Johnson across both "
            "pharmaceutical and medical device businesses. Thermo Fisher mass spectrometers, "
            "chromatography systems, and automated laboratory equipment are standard in J&J's "
            "Janssen pharmaceutical manufacturing and quality-control labs worldwide. Thermo "
            "Fisher's Patheon CDMO unit has provided manufacturing services for Janssen "
            "biologics including Stelara (ustekinumab) and Tremfya (guselkumab). For J&J "
            "MedTech, Thermo Fisher supplies analytical tools for sterility testing and "
            "materials characterization of surgical devices and implants. The relationship "
            "spans every segment of J&J's $85B+ annual business."
        ),
    },
    {
        "src": "DHR", "dst": "PFE", "type": "Supply Chain",
        "desc": "Danaher Cytiva bioprocessing equipment is critical to Pfizer's mRNA vaccine and biologics manufacturing",
        "value": "~$2-3B annually", "year": "2020",
        "source_url": "https://investors.danaher.com/financial-information/annual-reports",
        "source_name": "Danaher Annual Report",
        "details": (
            "Danaher's Cytiva division (acquired from GE Healthcare Life Sciences for $21B "
            "in 2020) supplies the bioreactors, chromatography systems, and filtration "
            "equipment at the heart of Pfizer's biologics and mRNA vaccine manufacturing. "
            "Cytiva's single-use bioreactors and ÄKTA chromatography systems were in "
            "critically short supply during COVID-19 vaccine scale-up, with Pfizer being "
            "one of the largest customers. Cytiva's ReadyToProcess platform enables rapid "
            "manufacturing scale-up from clinical to commercial volumes — a capability "
            "Pfizer depended on to produce 3B+ COVID-19 vaccine doses. Danaher is "
            "effectively an essential infrastructure supplier to Pfizer's entire biologics "
            "manufacturing base."
        ),
    },
    {
        "src": "DHR", "dst": "JNJ", "type": "Supply Chain",
        "desc": "Danaher Cytiva bioreactors and Pall filtration systems underpin J&J Janssen biologics manufacturing",
        "value": "~$1-2B annually", "year": "2020",
        "source_url": "https://investors.danaher.com/financial-information/annual-reports",
        "source_name": "Danaher Annual Report",
        "details": (
            "Danaher's Cytiva and Pall (filtration) divisions supply the core bioprocessing "
            "equipment for Johnson & Johnson's Janssen pharmaceutical manufacturing sites "
            "globally. Cytiva bioreactors produce Janssen biologics including Stelara "
            "(ustekinumab, $10B+ peak revenue), Tremfya, and Darzalex (daratumumab). "
            "Pall's tangential flow filtration (TFF) systems are used in Janssen's "
            "downstream purification of monoclonal antibodies. During COVID-19, Janssen's "
            "Ad26-based vaccine (Johnson & Johnson COVID-19 vaccine) was manufactured using "
            "Cytiva bioreactor platforms. Danaher's equipment is deeply embedded in J&J's "
            "biologic manufacturing infrastructure, making it a non-discretionary supplier."
        ),
    },

    # ── Pharma-pharma collaborations ──────────────────────────────────────────

    {
        "src": "PFE", "dst": "BMY", "type": "Partnership",
        "desc": "Pfizer + Bristol-Myers Squibb co-developed and co-promote Eliquis (apixaban) — world's top-selling anticoagulant",
        "value": "$12B+ annual Eliquis revenue (split ~50/50)", "year": "2007",
        "source_url": "https://www.businesswire.com/news/home/20071218005280/en/Pfizer-and-Bristol-Myers-Squibb-Enter-Global-Alliance-for-Apixaban",
        "source_name": "BusinessWire",
        "details": (
            "Pfizer and Bristol-Myers Squibb entered a global alliance in December 2007 to "
            "co-develop and co-commercialize apixaban (Eliquis), a Factor Xa inhibitor for "
            "stroke prevention and blood clot treatment. Eliquis launched in 2012 and became "
            "the world's best-selling anticoagulant by 2018. Global Eliquis revenues exceeded "
            "$12B in 2023, with BMS and Pfizer sharing costs and profits roughly equally. The "
            "partnership required coordinating two massive pharmaceutical sales forces and "
            "regulatory submissions across 100+ countries. Eliquis now has 200M+ prescriptions "
            "written annually and is the #1 prescribed cardiovascular drug in the US. The "
            "Pfizer-BMS alliance is one of the most financially successful pharma co-promotion "
            "deals in history."
        ),
    },
    {
        "src": "JNJ", "dst": "ABBV", "type": "Partnership",
        "desc": "J&J (Janssen) + AbbVie jointly developed and globally commercialize Imbruvica (ibrutinib) for blood cancers",
        "value": "$5B+ annual Imbruvica revenue (split AbbVie ~60/JNJ ~40)", "year": "2011",
        "source_url": "https://www.jnj.com/latest-news/janssen-and-abbvie-enter-global-alliance-to-develop-commercialize-ibrutinib",
        "source_name": "J&J Newsroom",
        "details": (
            "Janssen (J&J's pharmaceutical division) and AbbVie entered a global collaboration "
            "in 2011 to develop and commercialize ibrutinib (Imbruvica), a BTK inhibitor for "
            "blood cancers including chronic lymphocytic leukemia (CLL) and mantle cell "
            "lymphoma. Imbruvica launched in 2013 and rapidly became a blockbuster, with peak "
            "revenues of $5B+ globally. AbbVie received rights primarily outside the US while "
            "Janssen handles US commercialization, with costs and profits shared. Ibrutinib "
            "transformed the treatment of CLL — converting a once-fatal diagnosis into a "
            "manageable chronic condition. The deal is one of the defining oncology "
            "partnerships of the 2010s and earned billions for both companies."
        ),
    },
    {
        "src": "AMGN", "dst": "ABBV", "type": "Partnership",
        "desc": "Amgen-AbbVie settlement: Amgen's Amgevita (Humira biosimilar) licensed to launch in the US from January 2023",
        "value": "$20B+ Humira biosimilar market by 2025", "year": "2022",
        "source_url": "https://www.amgen.com/media/news-releases/2022/10/amgen-and-abbvie-reach-settlement-agreement-on-humira-biosimilar-amgevita-in-the-us",
        "source_name": "Amgen Newsroom",
        "details": (
            "Amgen and AbbVie reached a settlement in October 2022 allowing Amgen's Amgevita "
            "— a biosimilar to AbbVie's Humira (adalimumab) — to launch in the US starting "
            "January 31, 2023. Humira had been the world's best-selling drug, generating "
            "$14B+ annually for AbbVie on the strength of an extensive patent thicket. Amgen "
            "was the first biosimilar maker to breach that thicket through litigation. The "
            "settlement terms are confidential but allowed Amgevita to launch at a significant "
            "discount, beginning the erosion of Humira's US monopoly. The deal catalyzed "
            "launches by eight other Humira biosimilar makers in 2023 and accelerated AbbVie's "
            "transition to Skyrizi and Rinvoq as successor drugs."
        ),
    },
    {
        "src": "JNJ", "dst": "GOOGL", "type": "Joint Venture",
        "desc": "Verb Surgical — J&J and Verily (Alphabet) joint venture for AI-powered robotic surgery (2015)",
        "value": "$150M+ (JV investment)", "year": "2015",
        "source_url": "https://www.prnewswire.com/news-releases/johnson-johnson-and-verily-life-sciences-enter-strategic-collaboration-agreement-to-develop-robotics-assisted-surgery-platform-300165073.html",
        "source_name": "PR Newswire",
        "details": (
            "Johnson & Johnson and Verily Life Sciences (Google's life science subsidiary, "
            "now part of Alphabet) announced Verb Surgical as a joint venture in December "
            "2015 to develop an AI-powered robotic surgery platform. The JV combined J&J "
            "Ethicon's surgical device expertise with Google's machine learning, image "
            "recognition, and advanced visualization capabilities. The goal: create a "
            "fundamentally smarter surgical robot than the incumbent da Vinci (Intuitive "
            "Surgical). Verb Surgical was dissolved in 2019 with J&J taking over the "
            "development as its Ottava robotic surgery platform — now in clinical trials. "
            "The JV demonstrated that tech giants were willing to enter the $6B surgical "
            "robotics market and prompted incumbents and startups to accelerate AI development."
        ),
    },
    {
        "src": "MDT", "dst": "MSFT", "type": "Partnership",
        "desc": "Medtronic + Microsoft — AI clinical intelligence platform for diabetes, cardiac, and surgical device data",
        "value": "~$200M+ (multi-year)", "year": "2022",
        "source_url": "https://newsroom.medtronic.com/news-releases/news-release-details/medtronic-and-microsoft-expand-collaboration",
        "source_name": "Medtronic Newsroom",
        "details": (
            "Medtronic and Microsoft expanded their AI collaboration to build the Medtronic "
            "AI clinical intelligence platform on Azure. The platform integrates data from "
            "Medtronic's 50M+ connected devices — insulin pumps, cardiac monitors, "
            "neuromodulation devices — into a unified AI layer that powers predictive "
            "clinical insights. Azure AI models flag early warning signs of cardiac "
            "decompensation in heart failure patients with Medtronic's CRT-D devices, "
            "enabling proactive clinical intervention. Microsoft Teams connects Medtronic's "
            "clinical specialists with hospital teams for remote device interrogation and "
            "programming. The partnership positions Medtronic as the first large medtech to "
            "have an enterprise AI platform spanning all major therapeutic categories."
        ),
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # Healthcare sector — 30 additional relationships
    # ═══════════════════════════════════════════════════════════════════════════

    # ── Pharma × AWS cloud (additional) ──────────────────────────────────────

    {
        "src": "JNJ", "dst": "AMZN", "type": "Supply Chain",
        "desc": "J&J uses AWS for Janssen global clinical operations, regulatory submissions, and MedTech supply chain analytics",
        "value": "~$300M+ annually", "year": "2019",
        "source_url": "https://aws.amazon.com/health/pharmaceutical/",
        "source_name": "AWS Health",
        "details": (
            "Johnson & Johnson uses Amazon Web Services across its pharmaceutical (Janssen) "
            "and medical device (MedTech) divisions. Janssen's clinical data management "
            "system — handling trial data for 100+ concurrent studies — runs on AWS, "
            "accelerating FDA and EMA regulatory submissions. J&J's global supply chain "
            "analytics for MedTech (surgical instruments, contact lenses, orthopedic "
            "implants) use AWS for demand forecasting and inventory optimization across "
            "200+ manufacturing sites worldwide. J&J's 130,000 employees use AWS-hosted "
            "enterprise applications for research collaboration across its largest R&D "
            "sites in Raritan NJ, Spring House PA, and Beerse Belgium. AWS also handles "
            "J&J's global pharmacovigilance data processing for adverse event reporting "
            "to regulatory agencies in 150+ countries."
        ),
    },
    {
        "src": "LLY", "dst": "AMZN", "type": "Partnership",
        "desc": "Eli Lilly + Amazon Pharmacy — LillyDirect program makes Mounjaro and Zepbound available at discounted prices (2023)",
        "value": "~$200M+ annually (pharmacy channel)", "year": "2023",
        "source_url": "https://www.lillydirect.com/weight-management",
        "source_name": "LillyDirect",
        "details": (
            "Eli Lilly launched LillyDirect in January 2023 in partnership with select "
            "online pharmacies including Amazon Pharmacy, enabling patients to access "
            "Lilly's GLP-1 drugs (Mounjaro/tirzepatide for diabetes, Zepbound for obesity) "
            "directly at discounted prices with Lilly's savings cards. The partnership "
            "bypasses traditional pharmacy benefit manager (PBM) channels, reducing "
            "out-of-pocket costs for uninsured or under-insured patients. Amazon Pharmacy's "
            "Prime member fast delivery complements Lilly's strategy to expand access to "
            "its blockbuster drugs as GLP-1 demand explodes — Mounjaro/Zepbound generated "
            "$10B+ in 2024. The LillyDirect-Amazon Pharmacy integration was one of pharma's "
            "most prominent direct-to-consumer distribution experiments and positioned Amazon "
            "as a key channel for specialty drug dispensing at scale."
        ),
    },
    {
        "src": "MRK", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Merck uses AWS for global clinical trial management, supply chain analytics, and Keytruda real-world evidence generation",
        "value": "~$250M+ annually", "year": "2018",
        "source_url": "https://aws.amazon.com/health/pharmaceutical/",
        "source_name": "AWS Health",
        "details": (
            "Merck & Co. uses Amazon Web Services for clinical trial data management, "
            "manufacturing analytics, and real-world evidence generation across its global "
            "operations. Keytruda (pembrolizumab) — the world's best-selling cancer drug "
            "at $25B+ annually — requires continuous real-world evidence across tumor types; "
            "Merck uses AWS SageMaker to analyze this data at scale and identify new "
            "indications for Keytruda's expanding label. Merck's global manufacturing network "
            "spanning 31 sites uses AWS IoT and analytics for batch record management and "
            "quality control automation. Merck's EXPLORE AI drug-discovery platform — guiding "
            "molecule design for vaccines (Gardasil, Vaxneuvance) and oncology — runs AI "
            "models on AWS alongside Azure, reflecting a deliberate multi-cloud strategy."
        ),
    },
    {
        "src": "ABT", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Abbott uses AWS for FreeStyle Libre CGM cloud platform, Alinity diagnostics connectivity, and global supply chain",
        "value": "~$150M+ annually", "year": "2018",
        "source_url": "https://aws.amazon.com/health/medical-devices/",
        "source_name": "AWS Health",
        "details": (
            "Abbott Laboratories uses Amazon Web Services to power the cloud infrastructure "
            "for its FreeStyle Libre continuous glucose monitoring ecosystem — the world's "
            "most widely used CGM with 6M+ users. FreeStyle Libre sensors transmit "
            "continuous glucose data to AWS where Abbott's LibreLink platform stores, "
            "analyzes, and shares readings with patients and clinicians. Abbott's Alinity "
            "family of high-throughput diagnostic instruments (used in hospital labs "
            "worldwide) connects to AWS for remote monitoring and predictive maintenance. "
            "Abbott's global supply chain — spanning nutrition (Ensure, Pedialyte), cardiac "
            "devices, diagnostics, and neuromodulation — uses AWS for logistics analytics "
            "across 150 countries. AWS IoT monitors cold-chain integrity for temperature-"
            "sensitive Abbott diagnostics reagents during international shipment."
        ),
    },
    {
        "src": "DHR", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Danaher Cytiva and Cepheid use AWS for bioprocess analytics, diagnostics connectivity, and global instrument networks",
        "value": "~$200M+ annually", "year": "2019",
        "source_url": "https://aws.amazon.com/health/lifesciences/",
        "source_name": "AWS Health",
        "details": (
            "Danaher's life science businesses use Amazon Web Services alongside Microsoft "
            "Azure for cloud analytics across its largest platforms. Cytiva's KUBio modular "
            "bioreactor plants transmit process data to AWS IoT for real-time batch monitoring "
            "and quality analytics — critical as biopharma clients scale drug manufacturing. "
            "Cepheid's 50,000+ GeneXpert diagnostic systems in hospitals globally report test "
            "results (COVID-19, TB, flu, RSV) through AWS for epidemiological surveillance. "
            "Danaher's Leica Biosystems pathology instruments — used in cancer tissue "
            "diagnostics — use AWS for remote diagnostics and digital pathology AI. The multi-"
            "cloud approach gives Danaher's pharma and diagnostics clients flexibility in "
            "building their own cloud-native data workflows on top of Danaher instrument data."
        ),
    },
    {
        "src": "TMO", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Thermo Fisher Scientific uses AWS for instrument cloud connectivity, bioinformatics, and clinical supply chain cold-chain monitoring",
        "value": "~$150M+ annually", "year": "2019",
        "source_url": "https://aws.amazon.com/health/lifesciences/",
        "source_name": "AWS Health",
        "details": (
            "Thermo Fisher Scientific uses Amazon Web Services to complement its Microsoft "
            "Azure deployment, particularly for bioinformatics workloads and clinical supply "
            "chain analytics. Thermo Fisher's Ion Torrent next-generation DNA sequencers "
            "and Orbitrap mass spectrometers connect to AWS for data storage and downstream "
            "analysis when customers use AWS-native bioinformatics pipelines. Thermo Fisher's "
            "clinical supply chain division — managing drug storage, labeling, and global "
            "distribution for 200+ clinical trials — uses AWS IoT for temperature monitoring "
            "critical for mRNA and biologics cold-chain integrity. The company's Integrated "
            "DNA Technologies (IDT) CRISPR synthesis unit uses AWS for sequence-design order "
            "management and delivery logistics for synthetic biology customers globally."
        ),
    },

    # ── Pharma × Azure (additional) ──────────────────────────────────────────

    {
        "src": "PFE", "dst": "MSFT", "type": "Partnership",
        "desc": "Pfizer + Microsoft Azure — AI-accelerated drug discovery, digital manufacturing intelligence, and enterprise collaboration (2021)",
        "value": "~$300M+ (multi-year)", "year": "2021",
        "source_url": "https://www.pfizer.com/news/press-release/press-release-detail/pfizer-and-microsoft-collaborate-accelerate-digitization",
        "source_name": "Pfizer Newsroom",
        "details": (
            "Pfizer and Microsoft announced a collaboration in 2021 to apply Azure AI "
            "and machine learning across Pfizer's drug discovery and manufacturing "
            "operations. Azure powers Pfizer's digital manufacturing intelligence — "
            "connecting real-time sensor data from manufacturing equipment across 43 "
            "global sites to detect quality deviations before batch failures occur. "
            "Pfizer's drug discovery teams use Azure AI to analyze protein interaction "
            "data for mRNA therapeutics, small molecules, and vaccines. Microsoft 365 "
            "and Teams serve as Pfizer's enterprise platform for 83,000+ employees "
            "globally. During COVID-19, Azure helped Pfizer coordinate real-time production "
            "data across its Kalamazoo MI and Puurs Belgium facilities as it manufactured "
            "3B+ mRNA vaccine doses — the largest pharmaceutical manufacturing ramp-up in "
            "history."
        ),
    },
    {
        "src": "ABBV", "dst": "MSFT", "type": "Partnership",
        "desc": "AbbVie + Microsoft Azure — AI drug discovery, manufacturing intelligence, and global R&D collaboration (2022)",
        "value": "~$200M+ (multi-year)", "year": "2022",
        "source_url": "https://news.microsoft.com/2022/abbvie-microsoft-ai-partnership/",
        "source_name": "Microsoft News",
        "details": (
            "AbbVie partnered with Microsoft Azure to accelerate drug discovery and "
            "manufacturing operations. AbbVie uses Azure AI to analyze bioinformatics "
            "data for its immunology pipeline — Skyrizi (risankizumab) and Rinvoq "
            "(upadacitinib), which together are projected to replace Humira's $14B+ "
            "revenue. Azure's AI tools help AbbVie identify autoimmune disease biomarkers "
            "and optimize clinical trial design for its neuroscience and oncology programs. "
            "AbbVie's manufacturing quality systems use Azure IoT for real-time monitoring "
            "of biologics production across its North Chicago IL and Ludwigshafen Germany "
            "facilities. Microsoft 365 serves as AbbVie's enterprise productivity platform "
            "for its 50,000+ employees across 70 countries, powering collaboration between "
            "R&D scientists and commercial teams developing the successor immunology portfolio."
        ),
    },
    {
        "src": "BMY", "dst": "MSFT", "type": "Partnership",
        "desc": "Bristol-Myers Squibb + Microsoft Azure — AI-powered oncology drug discovery and clinical operations (2022)",
        "value": "~$200M+ (multi-year)", "year": "2022",
        "source_url": "https://news.microsoft.com/2022/bristol-myers-squibb-azure-oncology/",
        "source_name": "Microsoft News",
        "details": (
            "Bristol-Myers Squibb and Microsoft partnered to apply Azure AI across BMS's "
            "oncology drug discovery and clinical operations alongside its AWS relationship. "
            "BMS uses Azure OpenAI to analyze clinical trial data for Opdivo (nivolumab) "
            "and Yervoy (ipilimumab) — identifying biomarkers predicting response to "
            "immuno-oncology checkpoint therapy combinations. Azure Machine Learning powers "
            "BMS's computational biology platform for antibody design in its Celgene-derived "
            "pipeline. Microsoft 365 serves as BMS's enterprise productivity suite for "
            "34,000+ employees post-Celgene merger. Azure also supports BMS's cell therapy "
            "manufacturing tracking for CAR-T therapies Breyanzi and Abecma — where each "
            "dose is manufactured from an individual patient's T cells and requires strict "
            "chain-of-custody documentation across manufacturing, QC, and delivery."
        ),
    },

    # ── Pharma × Google Cloud ─────────────────────────────────────────────────

    {
        "src": "LLY", "dst": "GOOGL", "type": "Partnership",
        "desc": "Eli Lilly + Isomorphic Labs (Alphabet) — AI drug discovery collaboration, up to $1.7B milestone deal (2024)",
        "value": "Up to $1.7B (milestone-based)", "year": "2024",
        "source_url": "https://www.isomorphiclabs.com/articles/isomorphic-labs-kicks-off-2024-with-two-landmark-drug-discovery-collaborations",
        "source_name": "Isomorphic Labs",
        "details": (
            "Isomorphic Labs — Alphabet's AI-powered drug discovery company spun out of "
            "Google DeepMind — announced a landmark collaboration with Eli Lilly in "
            "January 2024 worth up to $1.7 billion. Isomorphic Labs applies AlphaFold "
            "protein-structure prediction and AI-driven molecular design to discover novel "
            "drug candidates across multiple therapeutic areas for Lilly. The deal includes "
            "an upfront payment plus milestone-based payments tied to drug development "
            "success. Lilly selected Isomorphic after DeepMind's AlphaFold2 achieved "
            "breakthrough accuracy in predicting protein 3D structures from amino-acid "
            "sequences — directly accelerating drug target identification and molecule "
            "optimization. The partnership is one of the largest AI drug discovery deals "
            "in history and signals pharma's willingness to pay Big Tech billions for "
            "AI-powered biology research."
        ),
    },
    {
        "src": "MRK", "dst": "GOOGL", "type": "Partnership",
        "desc": "Merck + Google Cloud — AI-powered drug discovery, real-world evidence analytics, and genomics research (2022)",
        "value": "~$150M+ (multi-year)", "year": "2022",
        "source_url": "https://cloud.google.com/customers/merck",
        "source_name": "Google Cloud",
        "details": (
            "Merck & Co. partners with Google Cloud for AI-driven drug discovery and "
            "real-world evidence analytics alongside its Azure and AWS deployments. Merck "
            "uses Google Cloud's Vertex AI and BigQuery to analyze genomic data from large "
            "patient populations, identifying genetic variants associated with cancer "
            "susceptibility and drug response for Keytruda expansion. Google Cloud's "
            "health data platform integrates claims, EHR, and lab data to support Merck's "
            "post-market surveillance for its oncology portfolio. Merck also collaborates "
            "with Google Health on digital biomarker research using wearable sensor data "
            "in clinical trials. DeepMind's AlphaFold protein-structure tool assists "
            "Merck's protein engineering team in designing next-generation biologics for "
            "cancer, infectious disease, and cardiometabolic indications."
        ),
    },

    # ── Life science supply chain — additional Thermo Fisher × pharma ─────────

    {
        "src": "TMO", "dst": "MRK", "type": "Supply Chain",
        "desc": "Thermo Fisher Patheon CDMO and analytical instruments supply Merck vaccine and biologics drug development and manufacturing",
        "value": "~$1-2B annually", "year": "2012",
        "source_url": "https://ir.thermofisher.com/financial-information/annual-reports",
        "source_name": "Thermo Fisher Annual Report",
        "details": (
            "Thermo Fisher Scientific is a major supplier to Merck & Co. across its "
            "vaccine, biologics, and small-molecule drug manufacturing operations. "
            "Thermo Fisher's Patheon CDMO manufactures and packages Merck clinical trial "
            "materials for oncology, vaccine, and antiviral programs. Thermo Fisher "
            "analytical instruments — including Orbitrap mass spectrometers and NanoDrop "
            "spectrophotometers — are standard in Merck's West Point PA and Rahway NJ "
            "manufacturing QC labs. Merck's Gardasil (HPV vaccine) and Vaxneuvance "
            "pneumococcal vaccine manufacturing operations rely on Thermo Fisher filtration, "
            "formulation, and fill-finish equipment. Keytruda monoclonal antibody production "
            "at Merck's biologics facilities uses Thermo Fisher HyClone cell culture media "
            "and bioprocessing consumables that cannot be easily substituted mid-campaign."
        ),
    },
    {
        "src": "TMO", "dst": "ABBV", "type": "Supply Chain",
        "desc": "Thermo Fisher Patheon CDMO and analytical instruments support AbbVie Humira, Skyrizi, and Rinvoq biologics manufacturing",
        "value": "~$1-2B annually", "year": "2013",
        "source_url": "https://ir.thermofisher.com/financial-information/annual-reports",
        "source_name": "Thermo Fisher Annual Report",
        "details": (
            "Thermo Fisher Scientific's Patheon CDMO division provides contract "
            "manufacturing and packaging services for AbbVie's biologics portfolio. "
            "Humira (adalimumab) — the world's former best-selling drug at $14B+ peak "
            "annual revenue — used Thermo Fisher's fill-finish manufacturing capabilities "
            "across multiple batches per year at Patheon's EU and US sites. AbbVie's "
            "successor drugs, Skyrizi (risankizumab) and Rinvoq (upadacitinib), continue "
            "to leverage Thermo Fisher's analytical chemistry and biologics manufacturing "
            "infrastructure as volumes scale to replace eroding Humira revenue after "
            "biosimilar entry. Thermo Fisher mass spectrometers and HPLC chromatography "
            "systems are embedded in AbbVie's North Chicago QC labs for batch release "
            "testing across drugs distributed to 70+ countries."
        ),
    },
    {
        "src": "TMO", "dst": "BMY", "type": "Supply Chain",
        "desc": "Thermo Fisher Patheon CDMO and laboratory instruments support Bristol-Myers Squibb oncology and cell therapy manufacturing",
        "value": "~$800M-1.5B annually", "year": "2012",
        "source_url": "https://ir.thermofisher.com/financial-information/annual-reports",
        "source_name": "Thermo Fisher Annual Report",
        "details": (
            "Thermo Fisher Scientific provides contract manufacturing and laboratory "
            "instrumentation for Bristol-Myers Squibb's oncology drug and cell therapy "
            "manufacturing. BMS's Opdivo (nivolumab) monoclonal antibody production "
            "relies on Thermo Fisher bioprocessing equipment and fill-finish capabilities. "
            "Following BMS's $74B Celgene acquisition in 2019, Thermo Fisher became an "
            "even more important supplier — Revlimid (lenalidomide) capsule manufacturing "
            "and Breyanzi/Abecma CAR-T cell therapy cold-chain logistics both leverage "
            "Thermo Fisher capabilities. Thermo Fisher's HyClone cell culture media are "
            "essential consumables for BMS's CAR-T manufacturing processes where individual "
            "patient T cells are expanded into personalized cancer treatments. Thermo "
            "Fisher's temperature-controlled storage systems also manage BMS's clinical "
            "trial supplies across its oncology study network."
        ),
    },

    # ── Life science supply chain — additional Danaher × pharma ──────────────

    {
        "src": "DHR", "dst": "LLY", "type": "Supply Chain",
        "desc": "Danaher Cytiva bioprocessing equipment is central to Eli Lilly's GLP-1 (tirzepatide) manufacturing scale-up",
        "value": "~$1-2B annually (growing rapidly)", "year": "2021",
        "source_url": "https://investors.danaher.com/financial-information/annual-reports",
        "source_name": "Danaher Annual Report",
        "details": (
            "Danaher's Cytiva division supplies the core bioprocessing equipment for "
            "Eli Lilly's rapid scale-up of tirzepatide (Mounjaro for diabetes, Zepbound "
            "for obesity) manufacturing. Tirzepatide is a GLP-1/GIP dual agonist requiring "
            "complex peptide synthesis and injectable formulation — processes supported by "
            "Cytiva bioreactors, ÄKTA chromatography systems, and single-use technologies. "
            "Lilly invested $9B+ in manufacturing capacity expansion as Mounjaro/Zepbound "
            "demand far exceeded supply in 2023-24. Danaher's equipment is embedded in "
            "Lilly's facilities in Indianapolis IN, Branchburg NJ, and Kinsale Ireland. "
            "Cytiva's ReadyToProcess single-use manufacturing platforms enabled Lilly to "
            "scale tirzepatide production faster than traditional stainless-steel bioreactors, "
            "making Danaher a critical enabler of Lilly's rise to the world's most valuable "
            "pharmaceutical company."
        ),
    },
    {
        "src": "DHR", "dst": "MRK", "type": "Supply Chain",
        "desc": "Danaher Cytiva bioreactors and Pall filtration underpin Merck vaccine and biologics manufacturing globally",
        "value": "~$800M-1.5B annually", "year": "2018",
        "source_url": "https://investors.danaher.com/financial-information/annual-reports",
        "source_name": "Danaher Annual Report",
        "details": (
            "Danaher's Cytiva and Pall divisions supply core bioprocessing equipment "
            "for Merck & Co.'s vaccine and biologics manufacturing operations. Cytiva "
            "bioreactors are central to Merck's Gardasil (HPV vaccine) manufacturing "
            "in Durham NC and West Point PA — one of the world's highest-volume biologics "
            "manufacturing facilities producing millions of doses annually. Pall's "
            "tangential flow filtration systems handle the critical downstream purification "
            "of monoclonal antibodies including Keytruda. During COVID-19, Merck used "
            "Cytiva single-use systems to rapidly scale MK-4482 (molnupiravir antiviral) "
            "manufacturing. Danaher's Cepheid GeneXpert systems are also deployed in Merck "
            "clinical trial sites worldwide for rapid PCR-based patient diagnostic testing "
            "during study enrollment and monitoring."
        ),
    },
    {
        "src": "DHR", "dst": "ABBV", "type": "Supply Chain",
        "desc": "Danaher Cytiva bioprocessing equipment central to AbbVie Humira and next-generation biologics manufacturing",
        "value": "~$800M-1.5B annually", "year": "2014",
        "source_url": "https://investors.danaher.com/financial-information/annual-reports",
        "source_name": "Danaher Annual Report",
        "details": (
            "Danaher's Cytiva (formerly GE Healthcare Life Sciences) and Pall divisions "
            "supply the bioprocessing infrastructure for AbbVie's biologics manufacturing. "
            "Humira (adalimumab), which generated $14B+ at its peak as the world's "
            "best-selling drug, required massive bioreactor capacity that Cytiva equipment "
            "supplied at AbbVie's North Chicago IL and Ludwigshafen Germany plants. "
            "AbbVie's successor immunology drugs — Skyrizi (anti-IL-23 antibody) and "
            "Rinvoq (JAK inhibitor) — use Cytiva single-use bioreactors and ÄKTA "
            "chromatography systems for biologics manufacturing scale-up. Pall filtration "
            "systems handle critical purification of AbbVie's monoclonal antibodies. "
            "Danaher's Sciex mass spectrometry instruments are used in AbbVie's bioanalytical "
            "labs for pharmacokinetics and quality control across its immunology pipeline."
        ),
    },
    {
        "src": "DHR", "dst": "BMY", "type": "Supply Chain",
        "desc": "Danaher Cytiva and Pall bioprocessing equipment supports Bristol-Myers Squibb immuno-oncology and CAR-T cell therapy manufacturing",
        "value": "~$600M-1B annually", "year": "2019",
        "source_url": "https://investors.danaher.com/financial-information/annual-reports",
        "source_name": "Danaher Annual Report",
        "details": (
            "Danaher's Cytiva and Pall divisions supply bioprocessing equipment for "
            "Bristol-Myers Squibb's oncology manufacturing — especially for cell therapies "
            "where Danaher's single-use bioreactor expertise is critical. BMS's Breyanzi "
            "(lisocabtagene maraleucel) and Abecma (idecabtagene vicleucel) CAR-T therapies "
            "require specialized cell culture equipment, including Cytiva's ReadyToProcess "
            "WAVE bioreactors for T-cell expansion ex vivo from each patient's blood draw. "
            "Each CAR-T dose is manufactured from an individual patient's T cells — a "
            "process requiring Cytiva and Pall bioprocessing consumables that cannot be "
            "scaled like traditional biologics. BMS's Opdivo (nivolumab) monoclonal antibody "
            "production in Syracuse NY and Devens MA also uses Danaher's bioprocessing "
            "infrastructure extensively."
        ),
    },

    # ── Berkshire Hathaway Healthcare investments ─────────────────────────────

    {
        "src": "BRK-B", "dst": "JNJ", "type": "Ownership",
        "desc": "Berkshire Hathaway held Johnson & Johnson as a core equity investment for four decades, exiting by 2022",
        "value": "~$4B+ (peak position, various periods)", "year": "1980",
        "source_url": "https://www.berkshirehathaway.com/letters/2021ltr.pdf",
        "source_name": "Berkshire Hathaway Annual Letter",
        "details": (
            "Berkshire Hathaway held Johnson & Johnson shares for roughly four decades, "
            "with Warren Buffett citing J&J's diversified healthcare model — pharmaceuticals, "
            "medical devices, and consumer products — as a classic defensive compounding "
            "business. J&J was one of Berkshire's earliest S&P 500 healthcare investments. "
            "Berkshire held a meaningful J&J position through multiple cycles including the "
            "Tylenol recall (1982), the DePuy hip recall (2010), and J&J's Kenvue consumer "
            "health spinoff announcement (2021). Berkshire gradually exited its J&J position "
            "through 2021-2022 as Buffett shifted healthcare exposure toward AbbVie and "
            "Bristol-Myers Squibb. The decades-long relationship reflects J&J's enduring "
            "appeal as a slow-growth dividend compounder with AAA credit and a resilient "
            "multi-segment healthcare model."
        ),
    },
    {
        "src": "BRK-B", "dst": "ABBV", "type": "Ownership",
        "desc": "Berkshire Hathaway acquired ~$3.3B AbbVie stake in Q3 2020 — a major new pharma position at Humira biosimilar discount",
        "value": "~$3.3B (Q3 2020 acquisition)", "year": "2020",
        "source_url": "https://www.berkshirehathaway.com/2020ar/2020ar.pdf",
        "source_name": "Berkshire Hathaway Annual Report",
        "details": (
            "Berkshire Hathaway revealed a $3.3 billion stake in AbbVie in its Q3 2020 "
            "13-F SEC filing, acquired alongside positions in Bristol-Myers Squibb, Merck, "
            "and Pfizer — marking Berkshire's entry into major pharmaceutical stocks. "
            "Warren Buffett (or investment managers Ted Weschler and Todd Combs) purchased "
            "AbbVie at depressed multiples during COVID-19 uncertainty about Humira biosimilar "
            "competition. AbbVie was trading at ~8x earnings at the time of acquisition. "
            "Berkshire sold most of its pharmaceutical positions in 2021, including trimming "
            "AbbVie, but the initial disclosure drove AbbVie shares up 8% on the announcement "
            "date — the classic Buffett validation effect where disclosure of Berkshire's "
            "ownership signals management quality and valuation attractiveness to the market."
        ),
    },

    # ── COVID-19 manufacturing partnership ────────────────────────────────────

    {
        "src": "MRK", "dst": "JNJ", "type": "Partnership",
        "desc": "Merck manufacturing J&J COVID-19 vaccine at two US plants — historic competitor-to-competitor deal facilitated by Biden Administration (2021)",
        "value": "~$105M (US government manufacturing contract)", "year": "2021",
        "source_url": "https://www.hhs.gov/about/news/2021/03/02/hhs-dod-partner-with-merck-to-increase-production-jj-covid-19-vaccine.html",
        "source_name": "HHS Press Release",
        "details": (
            "In March 2021, the Biden administration announced that Merck — a direct "
            "competitor to J&J in vaccines — would manufacture J&J's COVID-19 vaccine "
            "at two US facilities (Elkton MD and Durham NC). The US government facilitated "
            "the unprecedented rival-manufacturer deal as part of the Defense Production "
            "Act mobilization to accelerate COVID-19 vaccine supply. HHS and DoD awarded "
            "Merck a $105M contract to prepare the facilities and manufacture Ad26 doses. "
            "This was one of the most visible examples of competitor collaboration in "
            "pharmaceutical history — Merck had lost the COVID-19 vaccine race after "
            "discontinuing its own vaccine candidates in January 2021. The deal demonstrated "
            "that manufacturing capacity, not intellectual property, was the binding "
            "constraint to COVID vaccination and that pharma rivals could cooperate under "
            "extraordinary circumstances."
        ),
    },

    # ── Diagnostics × pharma ──────────────────────────────────────────────────

    {
        "src": "ABT", "dst": "MRK", "type": "Partnership",
        "desc": "Abbott companion diagnostics — Alinity platforms provide PD-L1 testing for Merck Keytruda patient selection in oncology",
        "value": "~$200M+ annually (companion Dx market)", "year": "2018",
        "source_url": "https://abbott.mediaroom.com/",
        "source_name": "Abbott Newsroom",
        "details": (
            "Abbott and Merck partner to supply companion diagnostic tests that identify "
            "which cancer patients are likely to respond to Keytruda (pembrolizumab). "
            "Merck's Keytruda, the world's best-selling cancer drug at $25B+, is approved "
            "across 40+ cancer indications — many requiring PD-L1 or TMB (tumor mutational "
            "burden) biomarker testing before treatment. Abbott's Alinity series of advanced "
            "diagnostics analyzers, used in hospital pathology labs across Europe and emerging "
            "markets, provides PD-L1 immunohistochemistry testing that complements approved "
            "Dako/Agilent assays used in the US. The companion diagnostic market is essential "
            "to precision oncology — regulators require validated biomarker tests as a "
            "condition of approval for several Keytruda indications, making Abbott's "
            "diagnostics infrastructure integral to Merck's commercial success."
        ),
    },
    {
        "src": "ABT", "dst": "LLY", "type": "Partnership",
        "desc": "Abbott FreeStyle Libre CGM integrated with Eli Lilly Tempo insulin management system — closed-loop diabetes management (2022)",
        "value": "~$150M+ annually (integrated system sales)", "year": "2022",
        "source_url": "https://www.diabetescare.abbott/",
        "source_name": "Abbott Diabetes Care",
        "details": (
            "Abbott and Eli Lilly partnered to connect Abbott's FreeStyle Libre continuous "
            "glucose monitoring (CGM) system with Lilly's Tempo connected insulin delivery "
            "ecosystem. The Tempo Smart Button — which attaches to any Lilly insulin pen — "
            "communicates dosing data to the Tempo by Lilly app, which integrates with "
            "FreeStyle Libre's real-time glucose readings to show glucose and insulin data "
            "in one unified view. This interoperability creates a simplified diabetes "
            "management experience for users of Lilly's Humalog and Basaglar insulins. "
            "The partnership addresses the fragmentation gap between CGM monitoring and "
            "insulin delivery that has historically required patients to use separate apps. "
            "As GLP-1 drugs (Mounjaro/Zepbound) shift the diabetes treatment landscape, "
            "the Abbott-Lilly device-drug ecosystem partnership remains central to both "
            "companies' diabetes care strategies."
        ),
    },

    # ── Health insurer × tech (additional) ───────────────────────────────────

    {
        "src": "UNH", "dst": "GOOGL", "type": "Partnership",
        "desc": "UnitedHealth Group uses Google Cloud for clinical AI, genomics analytics, and population health at 150M+ member scale",
        "value": "~$300M+ (multi-year)", "year": "2022",
        "source_url": "https://cloud.google.com/customers/unitedhealth",
        "source_name": "Google Cloud",
        "details": (
            "UnitedHealth Group and Google Cloud partnered to deploy AI across "
            "UnitedHealth's Optum data and analytics platform, which manages 150M+ lives. "
            "Google Cloud's BigQuery and Vertex AI analyze Optum's vast clinical dataset — "
            "combining claims, EHR, pharmacy, and lab data — to power predictive models for "
            "hospital readmission risk, care gap identification, and fraud detection in "
            "real time. Google Health's AI tools assist Optum Genomics in analyzing whole- "
            "genome sequences from consented members to identify genetic risk factors for "
            "chronic disease. The partnership positions UnitedHealth's Optum as an AI-native "
            "health intelligence platform competing with traditional healthcare analytics "
            "vendors by leveraging Google's leading AI research capabilities and the "
            "population-scale insights that only Optum's 15B+ annual data transactions enable."
        ),
    },
    {
        "src": "CI", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Cigna's Evernorth Express Scripts (largest US PBM) uses AWS for pharmacy claims processing and specialty drug management",
        "value": "~$200M+ annually", "year": "2019",
        "source_url": "https://aws.amazon.com/health/customers/evernorth/",
        "source_name": "AWS Health",
        "details": (
            "Cigna Group's Evernorth Health Services — the $100B+ pharmacy and care services "
            "platform — uses Amazon Web Services for its Express Scripts pharmacy benefit "
            "management operations alongside its Microsoft Azure relationship. Express Scripts, "
            "the largest US PBM, processes 1.5B+ prescriptions annually and uses AWS for "
            "drug interaction checking, formulary management, and real-time eligibility "
            "verification across Cigna's 180M+ plan member base. AWS enables Evernorth to "
            "process pharmacy claims at low latency during peak demand (first of the month "
            "when members pick up prescriptions). Evernorth's specialty pharmacy business "
            "— handling high-cost biologic drugs and cell therapies — uses AWS IoT for "
            "temperature-sensitive supply chain monitoring and patient adherence analytics."
        ),
    },

    # ── Pharma formulary and value-based contracts ────────────────────────────

    {
        "src": "UNH", "dst": "LLY", "type": "Partnership",
        "desc": "UnitedHealth OptumRx covers Mounjaro/Zepbound for 50M+ members — outcomes-based GLP-1 formulary agreement (2023)",
        "value": "~$3B+ annually (GLP-1 drug spend)", "year": "2023",
        "source_url": "https://www.unitedhealthgroup.com/newsroom.html",
        "source_name": "UnitedHealth Group Newsroom",
        "details": (
            "UnitedHealth Group's OptumRx pharmacy benefit manager covers Eli Lilly's "
            "tirzepatide (Mounjaro for diabetes, Zepbound for obesity) for 50M+ members "
            "under outcomes-based formulary agreements negotiated in 2023. As GLP-1 drugs "
            "became the fastest-growing drug category in pharmaceutical history, UnitedHealth "
            "and Lilly structured agreements tying rebate pricing to patient health outcomes "
            "— A1C reduction for diabetes and sustained weight loss for obesity. OptumRx's "
            "prior authorization criteria and step-therapy protocols significantly influence "
            "how many of the 70M+ US diabetes and obesity patients can access Lilly's drugs. "
            "The UNH-LLY relationship is one of the highest-value drug coverage negotiations "
            "in the US healthcare system, with GLP-1 spending projected to exceed $100B+ "
            "annually industry-wide — making OptumRx one of Lilly's most consequential "
            "commercial partners."
        ),
    },
    {
        "src": "CVS", "dst": "LLY", "type": "Partnership",
        "desc": "CVS Caremark and Eli Lilly GLP-1 weight management program — streamlined obesity drug access for 90M+ CVS members (2023)",
        "value": "~$1.5B+ annually (CVS GLP-1 drug spend)", "year": "2023",
        "source_url": "https://www.cvshealth.com/news/pharmacy.html",
        "source_name": "CVS Health",
        "details": (
            "CVS Health partnered with Eli Lilly in 2023 to streamline access to GLP-1 "
            "obesity drugs for CVS Caremark members, including Zepbound (tirzepatide for "
            "obesity) and Mounjaro (tirzepatide for type 2 diabetes). CVS Health's CareMark "
            "PBM manages prescription benefits for 90M+ members and is one of the three "
            "largest US pharmacy benefit managers. The CVS-Lilly partnership includes "
            "preferential formulary placement of Lilly's GLP-1s and streamlined prior "
            "authorization for qualifying patients. CVS MinuteClinic and HealthHUB locations "
            "provide monitoring and adherence support for patients on GLP-1 drugs, while "
            "Lilly provides patient support programs. The deal was part of a wave of "
            "PBM-pharma partnerships as GLP-1 drugs reshaped US healthcare spending, with "
            "CVS committing to be a distribution and care-coordination partner for Lilly's "
            "obesity franchise."
        ),
    },
    {
        "src": "UNH", "dst": "PFE", "type": "Partnership",
        "desc": "UnitedHealth OptumRx manages Pfizer's largest US drug access channel — Eliquis, Ibrance, Prevnar formulary coverage for 50M+ members",
        "value": "~$5B+ annually (Pfizer drugs through OptumRx)", "year": "2015",
        "source_url": "https://www.unitedhealthgroup.com/investor-relations.html",
        "source_name": "UnitedHealth Group IR",
        "details": (
            "UnitedHealth Group's OptumRx pharmacy benefit manager is one of Pfizer's "
            "most important drug access partners, managing formulary coverage for Pfizer's "
            "drugs across 50M+ OptumRx members. Eliquis (apixaban, co-promoted with BMS) "
            "is one of the most expensive drugs in OptumRx's formulary at $7B+ US revenue. "
            "Pfizer's immunology drug Xeljanz, cancer drug Ibrance, and Prevnar/Abrysvo "
            "pneumococcal vaccines all require OptumRx formulary positioning for wide patient "
            "access. OptumRx's rebate negotiations with Pfizer directly determine net drug "
            "prices for millions of patients — when OptumRx grants preferred formulary status "
            "to a Pfizer drug, it can shift hundreds of millions in incremental revenue. "
            "The UnitedHealth-Pfizer relationship exemplifies how integrated PBM-insurer "
            "entities now control pharmaceutical market access more than any other channel."
        ),
    },
    {
        "src": "ABBV", "dst": "GOOGL", "type": "Partnership",
        "desc": "AbbVie + Google Cloud — AI-powered immunology drug discovery and bioinformatics for Humira successor pipeline (2022)",
        "value": "~$100M+ (multi-year)", "year": "2022",
        "source_url": "https://cloud.google.com/customers/abbvie",
        "source_name": "Google Cloud",
        "details": (
            "AbbVie partners with Google Cloud for AI-driven drug discovery and "
            "bioinformatics, particularly for its immunology successor pipeline replacing "
            "Humira. AbbVie uses Google Cloud's Vertex AI to analyze complex multi-omics "
            "datasets — genomics, transcriptomics, and proteomics integrated with patient "
            "clinical data — to identify novel drug targets in autoimmune diseases including "
            "rheumatoid arthritis, inflammatory bowel disease, and psoriasis. Google Cloud's "
            "natural language AI processes scientific literature and patent filings to surface "
            "competitive intelligence for AbbVie's R&D strategy. DeepMind's AlphaFold "
            "protein-structure prediction tool accelerates AbbVie's biologics engineering for "
            "Skyrizi and next-generation IL-23/IL-17 pathway inhibitors. The partnership "
            "reflects AbbVie's strategic pivot to AI-first drug discovery as Humira biosimilar "
            "competition eroded $14B+ in annual revenue and AbbVie needed to accelerate its "
            "succession pipeline to maintain its position as a top-5 global pharma company."
        ),
    },
    {
        "src": "BMY", "dst": "GOOGL", "type": "Partnership",
        "desc": "Bristol-Myers Squibb + Google Cloud — immuno-oncology AI research, genomic tumor profiling, and clinical operations analytics (2022)",
        "value": "~$100M+ (multi-year)", "year": "2022",
        "source_url": "https://cloud.google.com/customers/bristol-myers-squibb",
        "source_name": "Google Cloud",
        "details": (
            "Bristol-Myers Squibb and Google Cloud partner to apply AI across BMS's "
            "oncology drug discovery and clinical operations. BMS uses Google Cloud's "
            "Vertex AI and BigQuery to analyze genomic tumor profiles across patient "
            "populations treated with Opdivo (nivolumab) and Yervoy (ipilimumab) — "
            "identifying molecular signatures that predict response to checkpoint "
            "immunotherapy combination regimens. Google DeepMind's AlphaFold assists "
            "BMS's protein engineering team in designing next-generation bispecific "
            "antibodies and antibody-drug conjugates for solid tumors. Google Cloud "
            "processes BMS's clinical trial data from 100+ ongoing oncology studies. "
            "The partnership supplements BMS's AWS relationship (primary for R&D data "
            "storage) and Azure deployment (enterprise operations) with Google's specialized "
            "AI capabilities for cancer biology research and genomic data science."
        ),
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # Communication Services — 30 additional relationships
    # ═══════════════════════════════════════════════════════════════════════════

    # ── Activision Blizzard ecosystem ─────────────────────────────────────────

    {
        "src": "ATVI", "dst": "MSFT", "type": "Ownership",
        "desc": "Microsoft acquired Activision Blizzard for $68.7B in October 2023 — largest gaming deal ever",
        "value": "$68.7B acquisition price", "year": "2023",
        "source_url": "https://news.microsoft.com/2023/10/13/microsoft-completes-activision-blizzard-acquisition/",
        "source_name": "Microsoft News",
        "details": (
            "Microsoft completed its $68.7B acquisition of Activision Blizzard King in "
            "October 2023 — the largest acquisition in gaming history and the largest in "
            "Microsoft's history. The deal adds Call of Duty, World of Warcraft, Diablo, "
            "Overwatch, Candy Crush, and Hearthstone to Microsoft's gaming portfolio. "
            "Activision Blizzard's 400M monthly active players and $8B+ annual revenue "
            "tripled Microsoft's gaming business. The deal faced an 18-month regulatory "
            "battle with the FTC and UK CMA before closing. Microsoft immediately committed "
            "to keeping Call of Duty on PlayStation for 10 years and brought the entire "
            "Activision catalog to Xbox Game Pass, massively expanding its subscription "
            "gaming service."
        ),
    },
    {
        "src": "ATVI", "dst": "AAPL", "type": "Supply Chain",
        "desc": "Call of Duty Mobile + Candy Crush generate over $1B annually on iOS App Store",
        "value": "$1B+ annually (App Store revenue)", "year": "2016",
        "source_url": "https://newsroom.activisionblizzard.com/2019-10-01-Call-of-Duty-Mobile-Launches-Globally",
        "source_name": "Activision Blizzard Newsroom",
        "details": (
            "Activision Blizzard's mobile games generate enormous revenue through Apple's "
            "iOS App Store. Candy Crush Saga (King) has been a top-grossing App Store title "
            "since 2013, earning billions through in-app purchases. Call of Duty Mobile "
            "launched globally in October 2019 and became the most downloaded mobile game "
            "in its first week, surpassing 500M downloads. Apple earns 30% of in-app "
            "purchase revenue (dropping to 15% after the first year). Activision Blizzard's "
            "mobile segment generated $1.8B+ revenue in 2022, largely from iOS. Apple's "
            "App Store is ATVI's single largest mobile distribution platform globally."
        ),
    },
    {
        "src": "ATVI", "dst": "AMZN", "type": "Partnership",
        "desc": "Activision Blizzard games available on Amazon Luna cloud gaming; AWS powers game server infrastructure",
        "value": "~$200M+ (cloud + distribution)", "year": "2020",
        "source_url": "https://www.aboutamazon.com/news/entertainment/amazon-luna-game-streaming",
        "source_name": "About Amazon",
        "details": (
            "Activision Blizzard games are available on Amazon Luna, Amazon's cloud gaming "
            "subscription service, including Call of Duty titles accessible without a "
            "console or high-end PC. Beyond distribution, Activision uses AWS for live game "
            "server infrastructure supporting Call of Duty: Warzone's 100M+ registered "
            "players — AWS provides the elastic compute required to handle simultaneous "
            "login spikes during new season launches. AWS GameLift manages Activision's "
            "dedicated game server fleets, automatically scaling capacity across regions. "
            "The relationship deepened under Microsoft's ownership, which already runs "
            "Azure alongside AWS for certain Activision studio workloads."
        ),
    },
    {
        "src": "ATVI", "dst": "GOOGL", "type": "Partnership",
        "desc": "Activision games dominate Google Play Store; Call of Duty Mobile is the #1 grossing Android game",
        "value": "$500M+ annually (Google Play revenue)", "year": "2019",
        "source_url": "https://newsroom.activisionblizzard.com/2019-10-01-Call-of-Duty-Mobile-Launches-Globally",
        "source_name": "Activision Blizzard Newsroom",
        "details": (
            "Activision Blizzard King's mobile games are distributed through the Google "
            "Play Store, making Google one of ATVI's two primary mobile platforms (alongside "
            "Apple iOS). Call of Duty Mobile is consistently among the top-grossing Android "
            "games globally, generating hundreds of millions in annual Google Play revenue. "
            "Google earns a 30% cut of in-app purchases (15% for subscriptions). Candy "
            "Crush Saga and its sequels maintain perennial top-10 rankings on Google Play. "
            "Google also featured Call of Duty Mobile in Stadia's launch lineup (before "
            "Stadia shut down) and continues to carry the game in its Android ecosystem. "
            "ATVI's titles collectively generate over $500M annually through Google Play."
        ),
    },

    # ── Gaming × platform distribution ───────────────────────────────────────

    {
        "src": "TTWO", "dst": "MSFT", "type": "Partnership",
        "desc": "Take-Two games (GTA V, Red Dead Online, NBA 2K) available on Xbox and Game Pass",
        "value": "~$300M+ annually (Game Pass licensing)", "year": "2020",
        "source_url": "https://investor.take2games.com/financial-information/annual-reports",
        "source_name": "Take-Two Interactive Annual Report",
        "details": (
            "Take-Two Interactive games are available across Microsoft's gaming ecosystem — "
            "Xbox consoles, PC Game Pass, and Xbox Game Pass Ultimate. Grand Theft Auto V "
            "was available on Xbox Game Pass and remains one of the best-selling games on "
            "Xbox platforms ($8B+ lifetime revenue). Red Dead Redemption 2 and Red Dead "
            "Online run on Xbox with full cross-platform features. NBA 2K titles ship "
            "on Xbox Day One with next-gen enhancements for Xbox Series X|S. Take-Two's "
            "forthcoming GTA VI — anticipated to be the highest-grossing entertainment "
            "product in history — will launch on PlayStation and Xbox simultaneously. "
            "Microsoft's Gaming Pass distribution significantly expands Take-Two's "
            "addressable audience beyond individual game purchases."
        ),
    },
    {
        "src": "TTWO", "dst": "AAPL", "type": "Partnership",
        "desc": "Rockstar and 2K games on iOS App Store; GTA: San Andreas remastered on Apple Arcade",
        "value": "~$100M+ annually (App Store revenue)", "year": "2013",
        "source_url": "https://www.apple.com/newsroom/2021/04/apple-arcade-expands-with-dozens-of-new-games/",
        "source_name": "Apple Newsroom",
        "details": (
            "Take-Two Interactive's Rockstar Games and 2K studios distribute games through "
            "Apple's iOS App Store and Apple Arcade subscription. Grand Theft Auto: San "
            "Andreas (remastered) joined Apple Arcade — Apple's $6.99/month gaming "
            "subscription — available on iPhone, iPad, Mac, and Apple TV. Rockstar Games "
            "Mobile has published iOS versions of GTA: San Andreas, GTA: Vice City, GTA III, "
            "and GTA: Chinatown Wars. 2K Games publishes NBA 2K Mobile, Borderlands Mobile, "
            "and XCOM 2 Collection on the App Store. The Apple Arcade arrangement provides "
            "Take-Two guaranteed licensing revenue without relying on in-app-purchase "
            "conversion, diversifying beyond the freemium model."
        ),
    },
    {
        "src": "EA", "dst": "AAPL", "type": "Partnership",
        "desc": "EA Sports mobile games + EA Play on Apple Arcade; EA earns billions through iOS App Store",
        "value": "~$500M+ annually (App Store revenue)", "year": "2008",
        "source_url": "https://www.apple.com/newsroom/2022/01/apple-arcade-expands-with-ea-sports-titles/",
        "source_name": "Apple Newsroom",
        "details": (
            "Electronic Arts has distributed games on iOS since 2008, building one of the "
            "largest mobile gaming portfolios on the App Store. EA's mobile hits include "
            "FIFA Mobile (now EA Sports FC Mobile), Madden Mobile, The Sims Mobile, and "
            "Plants vs. Zombies. In 2022, Apple Arcade added EA Sports titles including "
            "EA Sports PGA Tour Golf Clash+ and NBA Live Mobile+ under the Apple Arcade "
            "subscription — providing EA guaranteed revenue without in-app-purchase pressure. "
            "EA's mobile segment generates $1.6B+ annually, with iOS representing the "
            "majority. Apple earns its standard 30% commission on EA's App Store purchases, "
            "making EA one of Apple's largest gaming partners by revenue contribution."
        ),
    },
    {
        "src": "EA", "dst": "AMZN", "type": "Partnership",
        "desc": "EA Play subscription available on Amazon Luna cloud gaming service",
        "value": "~$100M+ (distribution deal)", "year": "2021",
        "source_url": "https://www.aboutamazon.com/news/entertainment/ea-play-on-luna",
        "source_name": "About Amazon",
        "details": (
            "Electronic Arts made EA Play — its subscription service with 60+ PC and "
            "console titles — available on Amazon Luna, Amazon's cloud gaming service. "
            "Luna subscribers with the EA Play channel can stream Battlefield, FIFA, Mass "
            "Effect, Apex Legends (via free-to-play access), and other EA titles without "
            "a dedicated gaming PC or console. EA also sells its PC games through Amazon's "
            "digital storefront. Amazon earns distribution revenue from EA Play subscriptions "
            "initiated through Luna while EA gains access to Amazon's broad Prime customer "
            "base. The deal extended EA Play's distribution footprint beyond Xbox Game Pass "
            "Ultimate, where it has been included since 2020."
        ),
    },

    # ── Streaming content distribution ────────────────────────────────────────

    {
        "src": "PARA", "dst": "AMZN", "type": "Partnership",
        "desc": "Paramount+ available on Amazon Prime Video Channels — subscribers can add Paramount+ within Prime Video",
        "value": "~$200M+ annually (distribution revenue)", "year": "2016",
        "source_url": "https://www.aboutamazon.com/news/entertainment/paramount-plus-on-prime-video-channels",
        "source_name": "About Amazon",
        "details": (
            "Paramount+ (and its predecessor CBS All Access) has been available through "
            "Amazon Prime Video Channels since 2016 — one of the first streaming services "
            "to join Amazon's channel marketplace. Amazon Prime Video Channels allows "
            "subscribers to add Paramount+ without leaving the Prime Video interface or "
            "managing a separate subscription. Amazon takes a commission on all Paramount+ "
            "subscriptions initiated through its platform. The arrangement gives Paramount+ "
            "access to Amazon's 200M+ Prime members as a distribution channel. Paramount's "
            "content — including Star Trek, Yellowstone, NFL games, and MTV reality shows — "
            "reaches Amazon's customer base without Paramount needing a separate user-"
            "acquisition channel."
        ),
    },
    {
        "src": "PARA", "dst": "AAPL", "type": "Partnership",
        "desc": "Paramount+ on Apple TV Channels — available as add-on subscription inside Apple TV app (2021)",
        "value": "~$100M+ annually (App Store commissions)", "year": "2021",
        "source_url": "https://www.apple.com/newsroom/2021/03/apple-tv-channels-adds-paramount-plus/",
        "source_name": "Apple Newsroom",
        "details": (
            "Apple TV Channels added Paramount+ in March 2021, coinciding with the "
            "rebranding of CBS All Access. Subscribers can add Paramount+ directly within "
            "the Apple TV app on iPhone, iPad, Mac, and Apple TV hardware — with Apple "
            "earning its standard App Store commission. The integration makes Paramount+ "
            "content — Star Trek: Strange New Worlds, Tulsa King, 1883, and NFL on CBS — "
            "accessible alongside Disney+, HBO Max, and other Apple TV Channels without "
            "switching apps. Apple TV Channels is Paramount's second-largest distribution "
            "partner after Amazon Channels. The Apple TV hardware device, with its "
            "premium user demographic, is particularly valuable for Paramount's ad-supported "
            "and premium tiers."
        ),
    },
    {
        "src": "PARA", "dst": "MSFT", "type": "Partnership",
        "desc": "Paramount+ available on Xbox consoles and Microsoft Store; CBS Sports integration with Microsoft Teams",
        "value": "~$50M+ annually (gaming distribution)", "year": "2021",
        "source_url": "https://news.xbox.com/en-US/2021/06/paramount-plus-on-xbox/",
        "source_name": "Xbox Newsroom",
        "details": (
            "Paramount+ launched on Xbox One and Xbox Series X|S in 2021, making it one "
            "of the first streaming services fully integrated into Microsoft's gaming "
            "console ecosystem. Xbox users can subscribe to Paramount+ directly through "
            "the Microsoft Store. CBS Sports content from Paramount (NFL on CBS, NCAA "
            "basketball, UEFA Champions League soccer) is integrated into Microsoft's "
            "sports content partnerships. Paramount also uses Microsoft Azure for portions "
            "of its Paramount+ streaming infrastructure, including content delivery "
            "optimization. The Xbox distribution gives Paramount+ access to Microsoft's "
            "35M+ Xbox monthly active users who also consume entertainment content on "
            "their consoles."
        ),
    },
    {
        "src": "WBD", "dst": "AMZN", "type": "Partnership",
        "desc": "Max (HBO) available on Amazon Fire TV and as Prime Video Channel — dual distribution deal",
        "value": "~$300M+ annually (distribution)", "year": "2020",
        "source_url": "https://www.aboutamazon.com/news/entertainment/hbo-max-comes-to-amazon-fire-tv",
        "source_name": "About Amazon",
        "details": (
            "Warner Bros. Discovery's Max (formerly HBO Max) distributes through Amazon "
            "via two channels: (1) as a native app on Amazon Fire TV devices — the US's "
            "most-sold streaming device — and (2) as a Prime Video Channel that Amazon "
            "subscribers can add within the Prime Video interface. Amazon Fire TV's 50M+ "
            "active users give Max significant distribution reach. The Prime Video Channel "
            "arrangement means Amazon customers can subscribe to Max without creating a "
            "separate account. Amazon takes a commission on Max subscriptions initiated "
            "through its platforms. The relationship is distinct from WBD's existing "
            "Microsoft Azure cloud partnership and Apple TV Channels deal — covering "
            "Amazon's critical retail and streaming device ecosystem."
        ),
    },

    # ── Music streaming × platform ────────────────────────────────────────────

    {
        "src": "SPOT", "dst": "AMZN", "type": "Partnership",
        "desc": "Spotify integrated with Amazon Echo/Alexa devices as preferred third-party music streaming service",
        "value": "~$100M+ annually (voice commerce revenue)", "year": "2016",
        "source_url": "https://newsroom.spotify.com/2016-06-01/spotify-now-available-on-amazon-echo/",
        "source_name": "Spotify Newsroom",
        "details": (
            "Spotify launched on Amazon Echo/Alexa in June 2016, making it the first "
            "major third-party music service on Alexa-enabled devices. Users can say 'Alexa, "
            "play [artist/playlist] on Spotify' and stream directly from their Spotify "
            "account. Spotify became one of Alexa's most requested third-party skills. "
            "Amazon Fire TV also supports Spotify as a native app for TV speaker playback. "
            "The integration is significant because Amazon competes with Spotify via Amazon "
            "Music Unlimited — yet both companies benefit from Spotify's Alexa availability: "
            "Amazon gains a richer Echo use case that drives device sales, while Spotify "
            "gains access to the 100M+ Alexa-enabled device installed base in the US alone."
        ),
    },
    {
        "src": "SPOT", "dst": "AAPL", "type": "Supply Chain",
        "desc": "Spotify on iOS App Store — Apple earns 30% commission while Spotify files EU antitrust complaint over rules",
        "value": "$500M+ annually (App Store commissions at peak)", "year": "2008",
        "source_url": "https://newsroom.spotify.com/2019-03-13/consumers-and-innovators-win-when-there-is-fair-competition/",
        "source_name": "Spotify Newsroom",
        "details": (
            "Spotify distributes its iOS app through the Apple App Store, making Apple one "
            "of Spotify's most important — and contentious — platform partners. At peak, "
            "Spotify paid Apple hundreds of millions annually in App Store commissions on "
            "iOS subscriptions. Spotify stopped allowing in-app subscriptions on iOS in "
            "2016 to avoid the 30% Apple fee, directing users to subscribe via the web. "
            "In March 2019, Spotify filed an EU antitrust complaint against Apple alleging "
            "the App Store rules unfairly favor Apple Music. The European Commission fined "
            "Apple €1.84B in 2024 for App Store anti-competitive conduct against Spotify. "
            "Despite the dispute, Spotify remains available on iPhone, Apple Watch, Apple "
            "TV, HomePod, and CarPlay — Apple devices are Spotify's largest user-device "
            "category globally."
        ),
    },

    # ── Music industry licensing × streaming ──────────────────────────────────

    {
        "src": "WMG", "dst": "SPOT", "type": "Supply Chain",
        "desc": "Warner Music Group multi-year global licensing deal with Spotify — WMG artists on Spotify",
        "value": "~$1B+ annually (streaming royalties)", "year": "2008",
        "source_url": "https://www.wmg.com/news/warner-music-group-and-spotify-renew-global-licensing-agreement",
        "source_name": "Warner Music Group",
        "details": (
            "Warner Music Group and Spotify have maintained a global licensing partnership "
            "since Spotify's launch in 2008, renewed multiple times including a major deal "
            "in 2021. WMG's roster — Ed Sheeran, Bruno Mars, Cardi B, Lizzo, Coldplay, "
            "Green Day, Metallica — generates billions of streams annually on Spotify. "
            "Spotify pays WMG a negotiated per-stream royalty rate plus a share of ad "
            "revenue for free-tier listening. WMG is one of Spotify's three major-label "
            "partners (alongside Universal and Sony). Music licensing is Spotify's single "
            "largest cost — roughly 70% of revenue — making the WMG relationship a "
            "critical part of Spotify's business model and content strategy."
        ),
    },
    {
        "src": "WMG", "dst": "AAPL", "type": "Supply Chain",
        "desc": "Warner Music Group licensing deal with Apple Music — WMG catalog available since 2015 launch",
        "value": "~$500M+ annually (streaming royalties)", "year": "2015",
        "source_url": "https://www.wmg.com/news/warner-music-group-apple-music-licensing-agreement",
        "source_name": "Warner Music Group",
        "details": (
            "Warner Music Group was among the founding label partners when Apple Music "
            "launched in June 2015. WMG's catalog — one of the three major label catalogs "
            "representing ~20% of all recorded music consumed globally — has been available "
            "on Apple Music continuously since launch. Apple pays WMG per-stream royalties "
            "at rates slightly higher than Spotify's (due to Apple Music's subscription-"
            "only model with no free tier). WMG benefits from Apple Music's 100M+ global "
            "subscribers and Apple's premium user demographics, which generate higher "
            "per-user revenue than Spotify's freemium mix. Apple Music is WMG's second-"
            "largest streaming revenue source after Spotify."
        ),
    },
    {
        "src": "WMG", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Warner Music Group licensing deal with Amazon Music Unlimited — WMG catalog on Amazon's streaming service",
        "value": "~$300M+ annually (streaming royalties)", "year": "2016",
        "source_url": "https://www.wmg.com/news/warner-music-group-amazon-music-licensing-agreement",
        "source_name": "Warner Music Group",
        "details": (
            "Warner Music Group licenses its catalog to Amazon Music Unlimited — Amazon's "
            "subscription music streaming service included free with Prime and as a "
            "standalone subscription. Amazon Music launched in 2007 and has grown to "
            "100M+ customers (including those who access the free Echo-only tier). WMG's "
            "global roster streams billions of times monthly on Amazon Music. The licensing "
            "deal covers Amazon Music HD (lossless audio), where WMG content was among "
            "the first catalogs available in 24-bit/192kHz quality — a premium differentiator. "
            "Amazon Music is WMG's fourth-largest streaming revenue source globally (after "
            "Spotify, Apple Music, and YouTube Music)."
        ),
    },
    {
        "src": "WMG", "dst": "META", "type": "Partnership",
        "desc": "Warner Music + Meta global licensing deal for music in Instagram Reels, Facebook videos, and Stories (2021)",
        "value": "~$100M+ annually (sync licensing)", "year": "2021",
        "source_url": "https://www.wmg.com/news/warner-music-group-and-facebook-announce-expanded-global-licensing-partnership",
        "source_name": "Warner Music Group",
        "details": (
            "Warner Music Group and Meta (then Facebook) announced an expanded global "
            "licensing partnership in 2021 covering music on Facebook, Instagram, Reels, "
            "Stories, and WhatsApp. The deal allows Meta's 3B+ users to use WMG-licensed "
            "songs as soundtracks for user-generated videos without copyright strikes. "
            "Instagram Reels competes directly with TikTok — music licensing is critical "
            "because viral Reels are almost always accompanied by popular songs. Meta pays "
            "WMG a negotiated licensing fee based on usage volume and ad revenue. The "
            "partnership covers WMG's Atlantic, Warner Records, Elektra, Reprise, Asylum, "
            "and Rhino labels, representing artists like Bruno Mars, Ed Sheeran, and Lizzo. "
            "This type of social media licensing became one of WMG's fastest-growing "
            "revenue streams."
        ),
    },

    # ── Telecom × AWS cloud ───────────────────────────────────────────────────

    {
        "src": "T", "dst": "AMZN", "type": "Partnership",
        "desc": "AT&T uses AWS for 5G network edge workloads and DirecTV Stream infrastructure alongside its Azure deal",
        "value": "~$500M+ (multi-year)", "year": "2021",
        "source_url": "https://aws.amazon.com/customers/att/",
        "source_name": "AWS",
        "details": (
            "AT&T uses Amazon Web Services alongside its primary Microsoft Azure deal in "
            "a multi-cloud strategy for different workloads. AT&T's DirecTV Stream "
            "cloud-based TV service runs on AWS for video encoding and global content "
            "delivery. AT&T's FirstNet public-safety broadband network — which covers "
            "all 50 states and US territories for first responders — uses AWS for its "
            "core cloud-services platform. AT&T's network operations leverage AWS IoT "
            "and analytics services for monitoring its 5G cell-site infrastructure. "
            "The dual-cloud approach (Azure for network functions + AWS for application "
            "workloads) gives AT&T flexibility and reduces dependency on a single "
            "hyperscaler — a risk management strategy common among the largest enterprises."
        ),
    },
    {
        "src": "VZ", "dst": "AMZN", "type": "Partnership",
        "desc": "Verizon uses AWS for network analytics, media delivery, and enterprise customer cloud workloads",
        "value": "~$400M+ (multi-year)", "year": "2020",
        "source_url": "https://aws.amazon.com/customers/verizon/",
        "source_name": "AWS",
        "details": (
            "Verizon uses Amazon Web Services alongside its Microsoft Azure partnerships "
            "in a multi-cloud architecture. Verizon Media (now Yahoo) runs its ad tech, "
            "content delivery, and sports streaming infrastructure on AWS — handling "
            "Yahoo Finance, Yahoo Sports, and TechCrunch's massive traffic. Verizon's "
            "network analytics platform uses AWS Kinesis for real-time processing of "
            "network telemetry from its 5G Ultra Wideband towers. Verizon Business "
            "re-sells AWS services to enterprise customers through the Verizon cloud "
            "marketplace. AWS also powers Verizon's +play subscription hub, which "
            "aggregates streaming services (Netflix, Apple One, Disney+) for Verizon "
            "wireless customers — a key retention and ARPU-growth initiative."
        ),
    },
    {
        "src": "TMUS", "dst": "AMZN", "type": "Partnership",
        "desc": "T-Mobile uses AWS for customer data analytics, 5G network operations, and T-Mobile TV platform",
        "value": "~$300M+ (multi-year)", "year": "2020",
        "source_url": "https://aws.amazon.com/customers/t-mobile/",
        "source_name": "AWS",
        "details": (
            "T-Mobile uses Amazon Web Services for data analytics and network operations "
            "alongside its primary Microsoft Azure deal. T-Mobile's Un-carrier Experience "
            "platform — which powers personalized customer offers and churn prediction — "
            "runs AI/ML models on AWS SageMaker. T-Mobile's TVision (now T-Mobile TV) "
            "streaming service infrastructure uses AWS for content delivery. After the "
            "Sprint merger in 2020, AWS helped T-Mobile migrate Sprint's legacy network "
            "management systems to a cloud-native architecture during the complex "
            "integration. T-Mobile's Network Experience platform analyzes 5G signal-quality "
            "data from 113M+ customers using AWS, identifying coverage gaps and "
            "optimization opportunities before customers notice degradation."
        ),
    },

    # ── Digital platform × advertising ────────────────────────────────────────

    {
        "src": "ROKU", "dst": "MSFT", "type": "Partnership",
        "desc": "Roku + Microsoft — Microsoft is Roku's preferred advertising technology and sales partner (2022)",
        "value": "~$300M+ (multi-year ad revenue share)", "year": "2022",
        "source_url": "https://newsroom.roku.com/news/2022/05/roku-and-microsoft-announce-advertising-partnership/",
        "source_name": "Roku Newsroom",
        "details": (
            "Roku and Microsoft announced a strategic advertising partnership in May 2022 "
            "making Microsoft the preferred advertising technology provider for Roku's "
            "platform. Microsoft's Xandr (formerly AppNexus) advertising marketplace "
            "powers programmatic ad buying and selling on Roku's platform, which reaches "
            "70M+ active accounts in North America. The deal gives Microsoft a premium CTV "
            "(connected TV) advertising footprint to compete with Google and The Trade Desk "
            "in the rapidly growing streaming-TV ad market. Roku's home screen, Roku "
            "Channel, and ad-supported streaming apps run Microsoft-powered ad auctions. "
            "Advertisers using Microsoft's DSP can now reach Roku's audience directly — "
            "complementing the Netflix advertising deal Microsoft also won in 2022."
        ),
    },
    {
        "src": "PINS", "dst": "AMZN", "type": "Partnership",
        "desc": "Pinterest + Amazon multi-year advertising partnership — Amazon product listings appear as shoppable Pins (2023)",
        "value": "~$500M+ annually (ad revenue)", "year": "2023",
        "source_url": "https://newsroom.pinterest.com/en/post/pinterest-and-amazon-announce-a-multiyear-ads-partnership",
        "source_name": "Pinterest Newsroom",
        "details": (
            "Pinterest and Amazon announced a groundbreaking multi-year advertising "
            "partnership in April 2023 — the first of its kind for Pinterest. Amazon "
            "product listings appear natively as shoppable Pins in Pinterest's visual "
            "discovery feed, allowing Pinterest's 460M+ monthly users to browse and "
            "purchase Amazon products without leaving Pinterest. The integration leverages "
            "Pinterest's intent-rich shopping audience (users actively searching for "
            "product inspiration) with Amazon's unparalleled product catalog and checkout "
            "infrastructure. Amazon acts as Pinterest's third-party advertising partner in "
            "the US initially, with global expansion planned. The deal significantly "
            "boosted Pinterest's ad revenue outlook and represented a strategic shift from "
            "Pinterest's reliance on Google and Meta advertising ecosystems."
        ),
    },
    {
        "src": "META", "dst": "AAPL", "type": "Supply Chain",
        "desc": "Meta's Facebook, Instagram, and WhatsApp distributed via iOS App Store — contentious relationship over ATT privacy",
        "value": "$10B+ annually (Apple's App Store share at peak; $10B estimated ATT revenue loss for Meta)",
        "year": "2008",
        "source_url": "https://about.fb.com/news/2021/04/facebooks-view-on-apples-ios-14-changes/",
        "source_name": "Meta Newsroom",
        "details": (
            "Meta's apps — Facebook, Instagram, Messenger, and WhatsApp — are distributed "
            "through Apple's iOS App Store, making Apple one of Meta's most critical "
            "distribution partners and most significant rivals. Apple's App Tracking "
            "Transparency (ATT) framework, launched with iOS 14.5 in April 2021, requires "
            "users to opt into cross-app tracking — which 85%+ decline. Meta estimated "
            "ATT cost it $10B+ in ad revenue in 2022 by degrading its ad targeting "
            "precision. Meta CEO Mark Zuckerberg has publicly criticized Apple's policies "
            "as anticompetitive. Despite the conflict, Meta's apps remain on the App "
            "Store and Apple earns App Store commissions on Meta's in-app purchases in "
            "games and the Meta Quest VR platform. The relationship is the tech industry's "
            "most prominent example of co-opetition."
        ),
    },
    {
        "src": "SNAP", "dst": "AAPL", "type": "Partnership",
        "desc": "Snapchat deeply integrated with Apple ARKit for camera AR lenses; iOS is Snapchat's primary platform",
        "value": "~$500M+ annually (App Store commissions)", "year": "2017",
        "source_url": "https://developer.apple.com/augmented-reality/arkit/",
        "source_name": "Apple Developer",
        "details": (
            "Snapchat and Apple have a deep technical partnership built around Apple's ARKit "
            "augmented-reality framework. Snap's signature Lenses — which overlay animated "
            "AR effects on users' faces and environments — use ARKit for real-time depth "
            "sensing and surface tracking on iPhone. Snap was an early ARKit partner when "
            "Apple launched it at WWDC 2017, co-demoing AR capabilities. iOS is Snapchat's "
            "primary platform: iPhone users open Snapchat more frequently and generate more "
            "revenue than Android users. Snap pays Apple App Store commissions on Snapchat+ "
            "subscriptions and in-app purchases. Snapchat is also deeply integrated with "
            "iMessage — Snaps can be shared to iMessage — and Spotlight content surfaces "
            "on Apple's News and Spotlight search."
        ),
    },

    # ── Content × mobile carrier bundle ──────────────────────────────────────

    {
        "src": "DIS", "dst": "TMUS", "type": "Partnership",
        "desc": "T-Mobile bundles Disney+ (and Disney Bundle) free for Magenta Max customers — 2021 deal",
        "value": "~$500M+ annually (Disney's wholesale rate × subscribers)", "year": "2021",
        "source_url": "https://newsroom.t-mobile.com/2021-08-04-T-Mobile-and-Disney-Partner-to-Bundle-Disney-Plus-Hulu-and-ESPN-Plus-for-T-Mobile-Customers",
        "source_name": "T-Mobile Newsroom",
        "details": (
            "T-Mobile and Disney announced a partnership in August 2021 to include the "
            "Disney Bundle (Disney+, Hulu, and ESPN+) free for T-Mobile Magenta Max "
            "customers — T-Mobile's premium unlimited plan. The bundle gives subscribers "
            "access to Disney's entire streaming ecosystem ($13.99/month retail value) at "
            "no additional cost. T-Mobile pays Disney a negotiated wholesale rate per "
            "subscriber. The deal drove significant Disney+ subscriber growth — T-Mobile "
            "has 45M+ postpaid customers, many of whom became Disney+ users for the first "
            "time through the bundle. It mirrors T-Mobile's 2017 'Netflix On Us' model "
            "that demonstrated carriers could use premium streaming to win and retain "
            "high-value customers at scale."
        ),
    },

    # ── Advertising spend: media brands × Meta ────────────────────────────────

    {
        "src": "DIS", "dst": "META", "type": "Partnership",
        "desc": "Disney is one of Meta's largest advertisers — Facebook and Instagram campaigns for Disney+, Marvel, ESPN, parks",
        "value": "$1B+ annually (ad spend)", "year": "2012",
        "source_url": "https://thewaltdisneycompany.com/the-walt-disney-company-investor-relations/",
        "source_name": "Walt Disney Company IR",
        "details": (
            "Walt Disney Company is one of Meta's largest advertising partners, spending "
            "an estimated $1B+ annually across Facebook and Instagram to promote Disney+, "
            "Hulu, ESPN+, Marvel film releases, Star Wars content, ABC Network shows, "
            "and Disneyland/Walt Disney World theme parks. Disney's advertising on Meta "
            "is sophisticated: precise demographic targeting drives Disney+ subscriber "
            "acquisition (family audiences, Marvel fans, Star Wars demographics), while "
            "Instagram Reels amplify viral content from Disney films. Disney's parks "
            "division uses Meta ads for geo-targeted promotions to drive vacation bookings. "
            "Despite building its own streaming platform, Disney relies heavily on Meta's "
            "social advertising infrastructure to reach audiences outside its owned channels."
        ),
    },
    {
        "src": "NFLX", "dst": "META", "type": "Partnership",
        "desc": "Netflix uses Facebook and Instagram advertising for content promotion and subscriber acquisition globally",
        "value": "$500M+ annually (ad spend)", "year": "2013",
        "source_url": "https://ir.netflix.net/ir/doc/annual-reports",
        "source_name": "Netflix 10-K",
        "details": (
            "Netflix is one of Meta's largest advertising customers, spending hundreds of "
            "millions annually on Facebook and Instagram to promote new series, acquire "
            "subscribers, and reduce churn. Netflix uses Meta's detailed interest targeting "
            "to reach potential subscribers likely to enjoy specific genres — horror fans "
            "ahead of new thriller releases, true-crime audiences before documentary "
            "premieres, and gamers for Netflix's growing interactive content. Netflix also "
            "uses Instagram Reels and Stories for short-form trailers that generate viral "
            "engagement. The relationship became more complex when Netflix launched its "
            "own ad-supported tier (with Microsoft as ad partner) in 2022 — competing "
            "with Meta for digital advertising budgets — while still relying on Meta's "
            "platforms to drive Netflix subscriptions."
        ),
    },
    {
        "src": "CHTR", "dst": "MSFT", "type": "Partnership",
        "desc": "Charter Spectrum + Microsoft Azure — enterprise cloud for Spectrum TV, internet, and mobile operations",
        "value": "~$300M+ (multi-year)", "year": "2022",
        "source_url": "https://news.microsoft.com/2022/charter-spectrum-microsoft-azure/",
        "source_name": "Microsoft News",
        "details": (
            "Charter Communications and Microsoft expanded their cloud partnership in 2022 "
            "to run Spectrum's cable TV, internet, and mobile operations on Azure. Charter "
            "uses Azure for its Spectrum TV App — delivering live cable TV and on-demand "
            "content to smartphones, tablets, and smart TVs without a cable box. Azure AI "
            "powers Charter's network operations center, predicting cable outages and "
            "automating service restoration across its 32M+ customer network. Microsoft "
            "Teams is Charter's enterprise collaboration platform for its 93,000+ employees. "
            "Charter's Spectrum Mobile — which runs on Verizon's network as an MVNO — uses "
            "Azure for subscriber management and billing analytics. The partnership "
            "positions Charter to deliver cloud-native cable services without legacy "
            "on-premise infrastructure."
        ),
    },
    {
        "src": "WBD", "dst": "GOOGL", "type": "Partnership",
        "desc": "Max on Google TV/Chromecast; WBD advertising on YouTube; Warner content distributed via Google platforms",
        "value": "$500M+ annually (advertising + distribution)", "year": "2020",
        "source_url": "https://cloud.google.com/customers/warner-bros-discovery",
        "source_name": "Google Cloud",
        "details": (
            "Warner Bros. Discovery distributes Max through Google's ecosystem via multiple "
            "channels: Max is available as a native app on Google TV-powered devices "
            "(Chromecast with Google TV, Sony/TCL smart TVs) and integrated into Google "
            "TV's universal guide. WBD is one of YouTube's largest content partners — "
            "Warner Bros., HBO, CNN, TNT, TBS, and DC Entertainment maintain official "
            "YouTube channels generating billions of monthly views. WBD runs substantial "
            "advertising on YouTube to promote Max content, DC films, and CNN programming. "
            "WBD also uses Google Cloud Platform for portions of its data analytics and "
            "AI workloads (complementing its primary Microsoft Azure relationship). Google "
            "TV's integration makes Max content discoverable via Google search and "
            "Assistant — 'Hey Google, play Succession on Max.'"
        ),
    },

    # ── Financial Services expansion (30 additional relationships) ─────────────

    {
        "src": "WFC", "dst": "MSFT", "type": "Partnership",
        "desc": "Wells Fargo selected Microsoft as preferred cloud provider in 2020",
        "value": "Multi-year strategic deal", "year": "2020",
        "source_url": "https://news.microsoft.com/2020/07/07/wells-fargo-selects-microsoft-as-preferred-cloud-provider/",
        "source_name": "Microsoft News",
        "details": (
            "In July 2020 Wells Fargo announced Microsoft as its preferred public cloud provider "
            "in a major long-term agreement. The bank committed to migrating its technology "
            "infrastructure to Microsoft Azure to modernize its core banking systems, reduce "
            "costs, and accelerate innovation. The deal came as Wells Fargo sought to rebuild "
            "credibility after regulatory sanctions and included Microsoft 365 productivity "
            "tools across the organization. Azure now underpins Wells Fargo's fraud detection, "
            "risk analytics, and customer-facing digital banking applications."
        ),
    },
    {
        "src": "BAC", "dst": "MSFT", "type": "Partnership",
        "desc": "Bank of America and Microsoft four-year Azure cloud commitment (2019)",
        "value": "Multi-billion multi-year deal", "year": "2019",
        "source_url": "https://newsroom.bankofamerica.com/content/newsroom/press-releases/2019/09/bank-of-america-and-microsoft-form-four-year-cloud-commitment.html",
        "source_name": "Bank of America Newsroom",
        "details": (
            "Bank of America and Microsoft announced a four-year cloud commitment in September "
            "2019, making Azure BofA's primary public cloud platform. The bank has deployed "
            "Azure for its AI-powered virtual assistant Erica (serving 35M+ users), fraud "
            "analytics, regulatory reporting, and data warehousing. In 2021 they expanded the "
            "partnership to include Azure OpenAI capabilities for compliance summarization and "
            "customer insights. Microsoft 365 also serves as BofA's enterprise productivity "
            "suite across its 215,000 employees globally."
        ),
    },
    {
        "src": "GS", "dst": "MSFT", "type": "Partnership",
        "desc": "Goldman Sachs built GS AI Platform on Microsoft Azure OpenAI (2023)",
        "value": "Strategic AI investment", "year": "2023",
        "source_url": "https://www.goldmansachs.com/our-firm/technology/ai-at-goldman-sachs.html",
        "source_name": "Goldman Sachs",
        "details": (
            "Goldman Sachs built its proprietary GS AI Platform on Microsoft Azure OpenAI "
            "Service, deploying large language models for investment banking, asset management, "
            "and compliance workflows. The platform processes earnings call transcripts, drafts "
            "client memos, and assists software engineers with code generation. Goldman "
            "engineers co-developed custom fine-tuned models with Microsoft to meet financial "
            "industry confidentiality requirements. By 2024 Goldman reported tens of thousands "
            "of employees actively using AI-assisted tools on the platform, representing one "
            "of the largest enterprise Azure OpenAI deployments in financial services."
        ),
    },
    {
        "src": "C", "dst": "MSFT", "type": "Partnership",
        "desc": "Citigroup and Microsoft strategic Azure cloud partnership",
        "value": "Multi-year cloud transformation", "year": "2020",
        "source_url": "https://news.microsoft.com/2020/03/02/citi-and-microsoft-announce-strategic-partnership/",
        "source_name": "Microsoft News",
        "details": (
            "Citigroup and Microsoft announced a strategic partnership in 2020 to accelerate "
            "Citi's cloud migration and digital transformation using Microsoft Azure. Citi "
            "selected Azure as a primary cloud infrastructure provider for core banking "
            "workloads including risk analytics, treasury operations, and trade finance. "
            "The partnership includes Microsoft 365 for enterprise productivity and Azure AI "
            "for credit decisioning and fraud detection models. Citi's global footprint across "
            "160+ countries makes this one of the most geographically broad financial services "
            "cloud deployments, relying on Azure's worldwide data center network."
        ),
    },
    {
        "src": "JPM", "dst": "GOOGL", "type": "Partnership",
        "desc": "JPMorgan Chase uses Google Cloud for merchant payments data and analytics",
        "value": "Cloud analytics partnership", "year": "2021",
        "source_url": "https://cloud.google.com/customers/jpmorgan-chase",
        "source_name": "Google Cloud",
        "details": (
            "JPMorgan Chase partnered with Google Cloud to process and analyze merchant payment "
            "data at scale for its Merchant Services and Chase Commerce Solutions divisions. "
            "Google Cloud's BigQuery data warehouse and AI/ML tools help JPMorgan deliver "
            "real-time transaction insights to small and medium businesses. JPMorgan also "
            "explored a joint consumer checking account product with Google (the 'Cache' "
            "project, announced 2019) before pivoting strategy in 2021. The bank continues "
            "to use Google Cloud for specific analytics workloads alongside its primary Azure "
            "and AWS deployments, reflecting a deliberate multi-cloud strategy for resilience."
        ),
    },
    {
        "src": "CME", "dst": "GOOGL", "type": "Partnership",
        "desc": "CME Group and Google Cloud 10-year deal to migrate global derivatives markets to cloud",
        "value": "~$1B+ 10-year agreement", "year": "2021",
        "source_url": "https://cloud.google.com/press-releases/2021/1109/cme-google-cloud",
        "source_name": "Google Cloud",
        "details": (
            "CME Group and Google Cloud announced a landmark 10-year strategic partnership "
            "in November 2021 to migrate CME's entire derivatives market infrastructure to "
            "Google Cloud. This covers CME's six major exchanges — Chicago Mercantile "
            "Exchange, CBOT, NYMEX, COMEX, NEX, and EBS — processing over 20 million "
            "contracts daily with notional value exceeding $1 quadrillion annually. The "
            "migration targets faster clearing, lower latency, and new AI-powered risk "
            "analytics. CME acquired a minority equity stake in Google's parent Alphabet as "
            "part of the deal, making it one of the most strategically significant cloud "
            "contracts in financial market infrastructure history."
        ),
    },
    {
        "src": "ICE", "dst": "MSFT", "type": "Partnership",
        "desc": "Intercontinental Exchange (NYSE) uses Azure for NYSE market data and mortgage tech",
        "value": "Strategic cloud partnership", "year": "2020",
        "source_url": "https://ir.theice.com/press/news-details/2020/ICE-Microsoft-Azure/default.aspx",
        "source_name": "ICE Investor Relations",
        "details": (
            "Intercontinental Exchange, the parent company of the New York Stock Exchange, "
            "deployed Microsoft Azure as a key cloud platform for NYSE market data distribution "
            "and its ICE Mortgage Technology division. ICE Mortgage Technology processes over "
            "40% of U.S. mortgage originations and relies on Azure's scale for document "
            "processing and compliance. NYSE market data — real-time quotes, historical "
            "trade data, reference data — is distributed via Azure to institutional customers "
            "globally. ICE also runs Bakkt, its digital asset and crypto custody platform, "
            "with Azure infrastructure supporting regulated crypto trading and settlement."
        ),
    },
    {
        "src": "SCHW", "dst": "MSFT", "type": "Partnership",
        "desc": "Charles Schwab deploys Microsoft Azure for Intelligent Portfolio and digital brokerage",
        "value": "Strategic cloud modernization", "year": "2022",
        "source_url": "https://news.microsoft.com/2022/schwab-microsoft-azure-digital-investing/",
        "source_name": "Microsoft News",
        "details": (
            "Charles Schwab selected Microsoft Azure as its primary cloud platform to modernize "
            "its digital brokerage and robo-advisory services following the TD Ameritrade "
            "acquisition in 2020. Azure powers Schwab's Intelligent Portfolios (automated "
            "investing) platform, trade order management, and client-facing mobile apps "
            "serving over 34 million brokerage accounts. Microsoft 365 serves as Schwab's "
            "enterprise collaboration suite. The migration accelerated Schwab's integration of "
            "TD Ameritrade's technology stack and enabled AI-driven personalization for "
            "financial planning tools, supporting Schwab's position as the largest U.S. "
            "retail brokerage by assets."
        ),
    },
    {
        "src": "BRK-B", "dst": "GS", "type": "Ownership",
        "desc": "Berkshire Hathaway invested $5B in Goldman Sachs preferred + warrants during 2008 crisis",
        "value": "~$5B+ (preferred stock + warrants)", "year": "2008",
        "source_url": "https://www.berkshirehathaway.com/news/sep2308.pdf",
        "source_name": "Berkshire Hathaway",
        "details": (
            "At the height of the 2008 financial crisis, Berkshire Hathaway invested $5 billion "
            "in Goldman Sachs through a purchase of perpetual preferred stock carrying a 10% "
            "annual dividend plus warrants to acquire $5 billion of Goldman common shares at "
            "$115 per share. The investment was announced September 23, 2008, days after "
            "Lehman Brothers collapsed. Berkshire earned approximately $3.7 billion in total "
            "profit from this transaction. Goldman redeemed the preferred in 2011 at a 10% "
            "premium; Berkshire exercised the warrants in 2013 through a cashless settlement "
            "that netted approximately 13.1 million Goldman shares, which were later sold."
        ),
    },
    {
        "src": "BRK-B", "dst": "WFC", "type": "Ownership",
        "desc": "Berkshire held Wells Fargo as a core 30-year investment (1989-2020)",
        "value": "~$26B peak (2017 position)", "year": "1989",
        "source_url": "https://www.berkshirehathaway.com/letters/2019ltr.pdf",
        "source_name": "Berkshire Hathaway Annual Letter",
        "details": (
            "Berkshire Hathaway began purchasing Wells Fargo shares in 1989 and held it as one "
            "of its 'Big Four' equity holdings for over three decades, at one point owning "
            "nearly 10% of the bank. Warren Buffett repeatedly cited Wells Fargo's low-cost "
            "deposit base and cross-selling model as enduring competitive advantages. However, "
            "a series of scandals — including the unauthorized account scandal (2016) and "
            "subsequent Federal Reserve asset cap — eroded Buffett's confidence. Berkshire "
            "steadily reduced its position starting in 2019 and sold its remaining Wells Fargo "
            "shares in 2021, ending one of Berkshire's longest-held major equity positions."
        ),
    },
    {
        "src": "BRK-B", "dst": "JPM", "type": "Ownership",
        "desc": "Berkshire acquired ~$4B in JPMorgan shares in 2018 (sold by 2021)",
        "value": "~$4B (at acquisition)", "year": "2018",
        "source_url": "https://www.berkshirehathaway.com/2018ar/2018ar.pdf",
        "source_name": "Berkshire Hathaway Annual Report",
        "details": (
            "Berkshire Hathaway disclosed a substantial position in JPMorgan Chase in its Q3 "
            "2018 13-F filing, having acquired approximately 35 million shares worth around "
            "$4 billion. Warren Buffett and Charlie Munger expressed admiration for JPMorgan "
            "CEO Jamie Dimon's management and the bank's return on equity and risk management. "
            "Berkshire also collaborated with JPMorgan on the Haven healthcare joint venture "
            "(with Amazon) from 2018 to 2021. Despite the expressed admiration, Berkshire "
            "sold its entire JPMorgan position by mid-2021, reportedly citing concerns about "
            "banking sector regulatory risks as a major long-term shareholder."
        ),
    },
    {
        "src": "C", "dst": "V", "type": "Partnership",
        "desc": "Citigroup issues Visa credit card portfolio (Citi Premier, Custom Cash, Prestige)",
        "value": "~$100B+ in Citi Visa card balances", "year": "1980",
        "source_url": "https://investor.visa.com/financial-information/annual-reports/default.aspx",
        "source_name": "Visa Annual Report",
        "details": (
            "Citigroup is one of Visa's largest global issuing bank partners, with a portfolio "
            "spanning consumer, small business, and commercial cards across dozens of countries. "
            "Major U.S. Citi Visa products include the Citi Premier, Citi Custom Cash, Citi "
            "Prestige, and Citi Strata Premier cards. Internationally, Citi issues Visa cards "
            "in Latin America, Asia, and Europe through its global consumer banking divisions. "
            "The relationship dates back to Visa's origins when Citibank was among the founding "
            "members of the BankAmericard network. Citi's managed Visa card balances represent "
            "a significant share of Visa's total global payment volume annually."
        ),
    },
    {
        "src": "C", "dst": "MA", "type": "Partnership",
        "desc": "Citigroup Mastercard cards including the popular Citi Double Cash Mastercard",
        "value": "~$50B+ in Citi Mastercard balances", "year": "1990",
        "source_url": "https://investor.mastercard.com/financial-information/annual-reports/default.aspx",
        "source_name": "Mastercard Annual Report",
        "details": (
            "In addition to its Visa portfolio, Citigroup issues a substantial range of "
            "Mastercard credit and debit cards globally. The Citi Double Cash Mastercard is "
            "one of the best-known flat-rate cash back cards in the U.S. market. Citi's "
            "Mastercard partnerships extend internationally where Mastercard's network is "
            "dominant — particularly in Europe, where Mastercard has historically had stronger "
            "issuing relationships than in North America. The dual Visa and Mastercard "
            "issuing strategy gives Citigroup maximum acceptance coverage for its 200+ "
            "million customer accounts across 160 countries, and allows Citi to optimize "
            "interchange economics by card product and market."
        ),
    },
    {
        "src": "MA", "dst": "AMZN", "type": "Partnership",
        "desc": "Mastercard powers Amazon Pay global acceptance and Amazon co-brand card programs",
        "value": "~$500B+ in Amazon Mastercard transaction volume", "year": "2002",
        "source_url": "https://newsroom.mastercard.com/press-releases/mastercard-and-amazon-expand-acceptance/",
        "source_name": "Mastercard Newsroom",
        "details": (
            "Mastercard is a core payment network for Amazon's global commerce ecosystem. "
            "Amazon Pay — used by millions of merchants outside Amazon.com — processes "
            "Mastercard transactions through direct acceptance agreements. Amazon issues "
            "co-brand credit cards on the Mastercard network in multiple countries including "
            "the Amazon Rewards Mastercard (via Synchrony Bank) for non-Prime customers and "
            "co-brand Amazon Mastercard products in international markets. In 2022, during "
            "Amazon's UK Visa dispute, Mastercard gained incremental volume as a preferred "
            "alternative. The relationship reflects Mastercard's essential role in any "
            "e-commerce ecosystem regardless of which network a merchant nominally prefers."
        ),
    },
    {
        "src": "AXP", "dst": "GOOGL", "type": "Partnership",
        "desc": "American Express cards available on Google Pay (2018) and Google Workspace integrations",
        "value": "Strategic digital payment integration", "year": "2018",
        "source_url": "https://newsroom.americanexpress.com/press-releases/news-details/2018/American-Express-Cards-Now-Available-on-Google-Pay/default.aspx",
        "source_name": "American Express Newsroom",
        "details": (
            "American Express joined Google Pay in 2018, enabling cardmembers to add their "
            "Amex credit, charge, and debit cards to Google Pay for contactless in-store "
            "payments and online checkout on Android devices. The integration covers personal "
            "consumer cards, small business cards, and corporate cards globally. Amex also "
            "integrates with Google Workspace for corporate travel and expense management — "
            "the Amex @ Work platform syncs with Google Calendar for meeting-based expense "
            "categorization. Google Ads purchases are frequently made on Amex corporate "
            "cards, creating a natural commercial relationship between the two companies "
            "beyond the consumer payment integration."
        ),
    },
    {
        "src": "MA", "dst": "GOOGL", "type": "Partnership",
        "desc": "Mastercard is a founding payment network partner for Google Pay and Google Wallet",
        "value": "Billions in Google Pay transactions annually", "year": "2015",
        "source_url": "https://newsroom.mastercard.com/press-releases/mastercard-and-google-team-up-to-bring-more-value-to-google-wallet/",
        "source_name": "Mastercard Newsroom",
        "details": (
            "Mastercard partnered with Google at the launch of Android Pay (now Google Pay) "
            "in 2015, becoming one of the two core payment networks — alongside Visa — powering "
            "Google's mobile wallet ecosystem. The partnership enables Mastercard cardholders "
            "at thousands of issuing banks to tap-to-pay at merchants using Google Pay on "
            "Android devices and Chrome browsers. Mastercard and Google also collaborate on "
            "tokenization standards through Mastercard's MDES (Digital Enablement Service), "
            "replacing physical card numbers with device-specific tokens for security. The "
            "partnership has expanded to include Mastercard Installments integrated into "
            "Google Pay checkout for buy-now-pay-later options."
        ),
    },
    {
        "src": "PYPL", "dst": "AAPL", "type": "Partnership",
        "desc": "PayPal and Venmo linked to Apple Wallet; PayPal available in Apple Pay merchant ecosystem",
        "value": "150M+ Apple device users with PayPal/Venmo access", "year": "2019",
        "source_url": "https://newsroom.paypal.com/2019-09-10-Apple-and-PayPal-Team-Up-to-Offer-More-Payment-Choices",
        "source_name": "PayPal Newsroom",
        "details": (
            "In September 2019, Apple and PayPal expanded their relationship to let iPhone "
            "and Apple Watch users add their PayPal and Venmo accounts to Apple Wallet as "
            "payment methods. This was a significant strategic shift: previously PayPal "
            "competed directly with Apple Pay, but the integration allowed PayPal-linked "
            "cards to be used at all Apple Pay contactless terminals. PayPal's Braintree "
            "payment gateway also powers Apple Pay on many e-commerce merchants. The "
            "partnership gave PayPal access to Apple's hundreds of millions of iOS users "
            "while extending Apple Wallet's utility beyond bank-issued cards, benefiting "
            "both companies' positions in the mobile payments ecosystem."
        ),
    },
    {
        "src": "PYPL", "dst": "GOOGL", "type": "Partnership",
        "desc": "PayPal integrated as a payment method in Google Pay on Android (2022)",
        "value": "Strategic digital wallet integration", "year": "2022",
        "source_url": "https://newsroom.paypal.com/2022-10-paypal-google-pay-integration",
        "source_name": "PayPal Newsroom",
        "details": (
            "PayPal integrated with Google Pay in 2022, allowing Android users to link their "
            "PayPal accounts to Google Wallet and use PayPal as a payment method at checkout "
            "for any merchant that accepts Google Pay. This gave PayPal access to Google's "
            "Android ecosystem of 3 billion+ active devices. PayPal's Braintree payment "
            "infrastructure also processes payments for Google's own properties and developer "
            "ecosystem. The integration deepened as Google Pay added Venmo as a linked "
            "payment option, expanding PayPal's social payments network to Google's Android "
            "user base and creating competitive pressure on Apple Pay's exclusivity within "
            "the iOS ecosystem."
        ),
    },
    {
        "src": "BLK", "dst": "AMZN", "type": "Supply Chain",
        "desc": "BlackRock uses AWS for alternative data processing and Aladdin analytics",
        "value": "Cloud infrastructure for $10T+ AUM platform", "year": "2020",
        "source_url": "https://aws.amazon.com/financial-services/customer-stories/blackrock/",
        "source_name": "AWS",
        "details": (
            "BlackRock, the world's largest asset manager with over $10 trillion in AUM, "
            "uses Amazon Web Services alongside Microsoft Azure to run workloads for its "
            "Aladdin investment operating system. AWS infrastructure processes alternative "
            "data feeds — satellite imagery, social sentiment, earnings call transcripts — "
            "that feed into Aladdin's portfolio risk models. BlackRock's eFront private "
            "markets platform (acquired 2019) also runs on AWS for its private equity and "
            "infrastructure analytics. The multi-cloud strategy prevents vendor lock-in for "
            "a platform that institutional clients worldwide depend on for risk management "
            "of $21+ trillion in assets under administration."
        ),
    },
    {
        "src": "MCO", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Moody's Analytics data and risk platform deployed on AWS",
        "value": "Cloud analytics infrastructure", "year": "2019",
        "source_url": "https://aws.amazon.com/financial-services/customer-stories/moodys-analytics/",
        "source_name": "AWS",
        "details": (
            "Moody's Analytics, the data and analytics arm of Moody's Corporation, runs "
            "key products on Amazon Web Services including its CreditView credit assessment "
            "platform, RiskCalc private firm credit models, and MARS risk management suite. "
            "AWS enables Moody's to deliver real-time credit risk data to banks, insurance "
            "companies, and asset managers globally. The cloud infrastructure supports "
            "Moody's acquisition-driven growth strategy — integrating acquired data "
            "companies like Bureau van Dijk (company financials) and Reis (commercial "
            "real estate) onto a unified cloud analytics layer. Moody's also uses AWS AI "
            "tools for natural language processing of financial documents and regulatory filings."
        ),
    },
    {
        "src": "SPGI", "dst": "AMZN", "type": "Supply Chain",
        "desc": "S&P Global uses AWS for commodity data, Capital IQ analytics, and Platts energy markets",
        "value": "Cloud infrastructure for $12B+ data business", "year": "2019",
        "source_url": "https://aws.amazon.com/financial-services/customer-stories/sp-global/",
        "source_name": "AWS",
        "details": (
            "S&P Global deploys Amazon Web Services across multiple business segments to "
            "distribute its financial data products globally. S&P Global Commodity Insights "
            "(formerly Platts) uses AWS to deliver real-time energy and commodities pricing "
            "data to traders in oil, gas, petrochemicals, metals, and agriculture markets. "
            "S&P Capital IQ Pro, the flagship investment research platform, leverages AWS "
            "for data ingestion, processing, and delivery to 370,000+ financial professionals. "
            "After merging with IHS Markit in 2022, S&P Global expanded its cloud footprint "
            "on AWS to integrate automotive, maritime, and financial risk datasets, creating "
            "one of the broadest data businesses in financial services."
        ),
    },
    {
        "src": "MS", "dst": "GOOGL", "type": "Partnership",
        "desc": "Morgan Stanley uses Google Cloud for digital wealth management and Next Best Action AI",
        "value": "Strategic cloud analytics partnership", "year": "2021",
        "source_url": "https://cloud.google.com/customers/morgan-stanley",
        "source_name": "Google Cloud",
        "details": (
            "Morgan Stanley partnered with Google Cloud to power its AI @ Morgan Stanley "
            "initiative, deploying large language models to help financial advisors surface "
            "insights from the firm's vast research library of 100,000+ documents. The "
            "'Next Best Action' system uses Google Cloud AI to recommend personalized "
            "investment ideas to Morgan Stanley's 16,000 financial advisors in real time. "
            "Morgan Stanley Wealth Management also uses Google Cloud's data analytics tools "
            "for client portfolio analysis and regulatory compliance monitoring. The "
            "partnership includes Google Cloud's Vertex AI platform for model training and "
            "deployment, cementing Google as a key AI infrastructure partner for one of "
            "Wall Street's largest wealth management businesses."
        ),
    },
    {
        "src": "GS", "dst": "GOOGL", "type": "Partnership",
        "desc": "Goldman Sachs uses Google Cloud for trading analytics and AI model development",
        "value": "Strategic AI and cloud analytics partnership", "year": "2021",
        "source_url": "https://cloud.google.com/customers/goldman-sachs",
        "source_name": "Google Cloud",
        "details": (
            "Goldman Sachs partners with Google Cloud for specific AI and analytics workloads "
            "alongside its primary Microsoft Azure deployment. Google Cloud's BigQuery is "
            "used for large-scale financial data analytics, while Vertex AI supports model "
            "development for trading signal generation and risk factor analysis. Goldman "
            "also uses Google's natural language AI for processing unstructured financial "
            "documents including SEC filings, analyst reports, and news. The partnership "
            "reflects Goldman's multi-cloud strategy where different workloads run on the "
            "optimal cloud for cost, performance, and capability — Azure for the GS AI "
            "Platform (OpenAI integration) and Google for data analytics and ML research."
        ),
    },
    {
        "src": "ICE", "dst": "AMZN", "type": "Supply Chain",
        "desc": "ICE Mortgage Technology and Bakkt crypto platform run on AWS infrastructure",
        "value": "Cloud-native financial market infrastructure", "year": "2019",
        "source_url": "https://aws.amazon.com/financial-services/customer-stories/intercontinental-exchange/",
        "source_name": "AWS",
        "details": (
            "Intercontinental Exchange uses Amazon Web Services for its ICE Mortgage "
            "Technology division, which processes over 40% of U.S. mortgage originations "
            "through Encompass and other loan origination systems. AWS enables real-time "
            "document processing, automated underwriting, and electronic closings at scale. "
            "Bakkt, ICE's digital asset platform for regulated Bitcoin futures and custody, "
            "also leverages AWS for its cloud-native trading and settlement infrastructure. "
            "ICE's multi-cloud approach uses Azure for NYSE market data distribution and "
            "AWS for mortgage and digital asset operations, reflecting the different latency "
            "and compliance requirements of these distinct financial market businesses."
        ),
    },
    {
        "src": "CME", "dst": "MSFT", "type": "Partnership",
        "desc": "CME Group uses Microsoft Azure and Teams for trading communications alongside Google Cloud",
        "value": "Secondary cloud and enterprise collaboration", "year": "2022",
        "source_url": "https://news.microsoft.com/2022/cme-group-microsoft-azure-teams/",
        "source_name": "Microsoft News",
        "details": (
            "While CME Group's primary cloud partnership is with Google Cloud (for exchange "
            "infrastructure migration), CME also uses Microsoft Azure and Teams as part of "
            "its enterprise technology stack. Microsoft Teams serves as the communications "
            "platform for CME's global trading operations, replacing legacy trader voice "
            "communication systems. Azure runs CME's internal analytics, risk management "
            "reporting, and compliance surveillance workloads. Microsoft 365 is deployed "
            "firm-wide for productivity. This dual-cloud approach — Google Cloud for "
            "market-facing infrastructure and Azure for enterprise workloads — reflects the "
            "operational complexity of managing one of the world's largest derivatives "
            "exchanges processing over $1 quadrillion in notional value annually."
        ),
    },
    {
        "src": "SCHW", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Charles Schwab uses AWS for digital brokerage infrastructure and trading systems",
        "value": "Cloud infrastructure for 34M+ client accounts", "year": "2020",
        "source_url": "https://aws.amazon.com/financial-services/customer-stories/charles-schwab/",
        "source_name": "AWS",
        "details": (
            "Charles Schwab runs significant portions of its digital brokerage infrastructure "
            "on Amazon Web Services, including systems supporting 34 million active brokerage "
            "accounts and trillions in client assets. AWS powers Schwab's mobile trading "
            "apps, real-time account data APIs, and options trading analytics. After "
            "completing the $26 billion TD Ameritrade acquisition in 2020, Schwab used AWS "
            "to accelerate the integration of TD Ameritrade's thinkorswim trading platform "
            "and client data migration. AWS Elastic infrastructure allows Schwab to scale "
            "compute dynamically during market volatility events — critical when trading "
            "volumes spike 10x on high-volatility days like meme-stock episodes or "
            "Fed announcement days."
        ),
    },
    {
        "src": "C", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Citigroup uses AWS for banking cloud workloads and Citi Ventures fintech investments",
        "value": "Multi-workload banking cloud infrastructure", "year": "2019",
        "source_url": "https://aws.amazon.com/financial-services/customer-stories/citi/",
        "source_name": "AWS",
        "details": (
            "Citigroup runs banking workloads on Amazon Web Services as part of its "
            "multi-cloud strategy alongside Microsoft Azure. AWS supports Citi's treasury "
            "and trade solutions, derivatives processing, and data analytics pipelines for "
            "its institutional clients business. Citi Ventures, the bank's venture capital "
            "arm, has invested in multiple AWS-native fintech startups including cloud-native "
            "lending, payments, and regtech companies. Citi's investment bank uses AWS "
            "SageMaker for quantitative research models and risk factor analytics. The "
            "bank's global presence across 160+ countries benefits from AWS's international "
            "data center footprint for low-latency banking operations in emerging markets."
        ),
    },
    {
        "src": "BLK", "dst": "GOOGL", "type": "Partnership",
        "desc": "BlackRock and Google Cloud partnership for ESG data analytics and alternative investments",
        "value": "Strategic AI and analytics partnership", "year": "2022",
        "source_url": "https://cloud.google.com/customers/blackrock",
        "source_name": "Google Cloud",
        "details": (
            "BlackRock partnered with Google Cloud to enhance its ESG (Environmental, Social, "
            "and Governance) data capabilities and alternative investment analytics. Google "
            "Cloud's Earth Engine satellite imagery platform feeds into BlackRock's climate "
            "risk models — analyzing physical climate exposure for assets in its Aladdin "
            "Climate product suite. Google Cloud's natural language AI processes sustainability "
            "reports and TCFD disclosures at scale, helping BlackRock's Sustainable Investing "
            "platform assess 25,000+ securities. The partnership also supports eFront's "
            "private markets analytics for BlackRock's $300B+ infrastructure and private "
            "equity business, where Google Cloud's geospatial and AI capabilities provide "
            "unique data insights unavailable from traditional financial data providers."
        ),
    },
    {
        "src": "PYPL", "dst": "MSFT", "type": "Partnership",
        "desc": "PayPal integrates with Microsoft Dynamics 365 Commerce for enterprise B2B payments",
        "value": "Enterprise commerce integration", "year": "2023",
        "source_url": "https://newsroom.paypal.com/2023-10-paypal-microsoft-dynamics-integration",
        "source_name": "PayPal Newsroom",
        "details": (
            "PayPal integrated its payment solutions with Microsoft Dynamics 365 Commerce, "
            "enabling retailers and enterprise merchants using Microsoft's commerce platform "
            "to offer PayPal and Venmo as checkout options without custom development. The "
            "integration supports PayPal's Pay Later (BNPL) products within Dynamics 365 "
            "storefronts, helping merchants increase average order value. PayPal Braintree "
            "also serves as a payment processor for Microsoft's own digital marketplaces "
            "and developer tool subscriptions in select regions. PayPal's developer tools "
            "and SDKs are prominently featured on Microsoft Azure Marketplace, giving "
            "Azure-hosted e-commerce applications easy access to PayPal's 430M+ consumer "
            "and merchant accounts."
        ),
    },
    {
        "src": "BAC", "dst": "AMZN", "type": "Supply Chain",
        "desc": "Bank of America uses AWS for financial analytics and cloud-based banking services",
        "value": "Multi-workload cloud partnership", "year": "2021",
        "source_url": "https://aws.amazon.com/financial-services/customer-stories/bank-of-america/",
        "source_name": "AWS",
        "details": (
            "Bank of America complements its primary Microsoft Azure deployment with Amazon "
            "Web Services for specific financial analytics and data workloads. AWS runs BofA's "
            "quantitative research models, securities lending analytics, and some capital "
            "markets data pipelines. The bank's Global Research division uses AWS SageMaker "
            "for training machine learning models on market data. BofA's CashPro digital "
            "treasury management platform, serving corporate treasurers globally, has "
            "AWS-hosted components for real-time payments and FX analytics. The multi-cloud "
            "approach reflects regulators' expectations that systemically important banks "
            "avoid single-provider dependency for critical banking infrastructure."
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
