# ESG Arcade: Real Estate Edition

![image](https://github.com/user-attachments/assets/27f2db71-224d-4e06-87f5-464507e45589)
![image](https://github.com/user-attachments/assets/5345c1b2-aeaa-4052-b85c-651b21f7d58f)
![image](https://github.com/user-attachments/assets/5838bc48-47e5-40a9-8949-4edcb32fd8af)
![image](https://github.com/user-attachments/assets/44f596f8-bbbe-4ea1-8e16-d3452334b367)





## What This Project Does

ESG Arcade is an interactive application that gamifies Environmental, Social, and Governance (ESG) integration for real estate portfolios. Using a retro gaming aesthetic, it helps property managers and community stakeholders:

- **Map and monitor** real estate portfolios through an interactive dashboard
- **Assess ESG performance** across environmental, social, and governance dimensions
- **Track progress** toward sustainability targets and regulatory compliance
- **Simulate retrofit projects** to improve building performance with budget constraints
- **Generate standardized reports** compatible with frameworks like GRESB, SFDR, GRI, and TCFD

The application transforms complex ESG data into accessible, engaging visualizations that make sustainability metrics approachable to all stakeholders, not just specialists.

## How It Works

ESG Arcade uses Streamlit to deliver a browser-based interface with:

1. **Interactive visualizations** built with Plotly and styled with retro gaming elements
2. **Data processing pipeline** for analyzing property metrics and calculating ESG scores
3. **Simulation engine** that calculates impact of potential retrofits on building performance
4. **Reporting framework** that aligns with international ESG standards
5. **Gamification elements** like points, levels, and achievements to encourage engagement

All components are styled with a pixel-perfect retro gaming aesthetic using custom CSS, making sustainability management more engaging than traditional corporate dashboards.

## Why This Project Matters in 2025

As we face 2025's intensifying climate crisis, stricter regulations, and growing social inequality:

- **New EU Sustainable Finance regulations** (SFDR Phase II, CSRD) now mandate comprehensive ESG reporting
- **The 2024 Global Climate Agreement** requires all buildings to reduce emissions 50% by 2030
- **Post-pandemic housing inequalities** have highlighted the need for socially responsible real estate
- **Investment capital** increasingly flows only to demonstrably sustainable projects
- **Energy price volatility** makes efficiency improvements economically essential

This tool arrives at a critical moment when collective action on building sustainability is no longer optional but required by law, economics, and planetary boundaries.

## Why This Project Matters From a Collective Perspective

This ESG (Environmental, Social, and Governance) application represents an important step toward creating housing and building systems that benefit everyone, not just property owners and investors.

### Environmental Justice

The environmental components of this application help buildings reduce:
- Carbon emissions that harm our shared atmosphere
- Energy waste that depletes our collective resources
- Water usage that impacts community resources

Every person, regardless of economic status, deserves clean air, water, and a stable climate. This tool promotes the responsible stewardship of our common environmental heritage.

### Social Equality

The social metrics tracked in this application focus on:
- Tenant wellbeing rather than just profit extraction
- Community impact assessment
- Creating spaces that serve human needs first

Housing and buildings should exist primarily to meet people's needs for shelter, work, and community gathering, not simply as vehicles for profit accumulation.

### Collective Governance

The governance tracking promotes:
- Transparent reporting and accountability
- Compliance with regulations that protect people and planet
- Long-term planning that considers future generations

When buildings and developments are managed with collective input and oversight, they better serve the needs of all people rather than just the wealthy few.

## Revolutionary Approach to Real Estate

This application transforms traditional profit-centered real estate analysis into a tool that measures what truly matters - how buildings serve people and planet. By gamifying these metrics, we make visible the real impacts of buildings on our shared existence.

The retro-gaming aesthetic reminds us that another world is possible - one where playfulness and community care replace exploitation and extraction.

## Practical Benefits

- Easily visualize which properties serve community needs vs. those that primarily extract wealth
- Track regulations that protect collective resources
- Prioritize retrofits that benefit residents and workers, not just owners
- Generate reports that hold property managers accountable to the community

## Installation and Usage

### Prerequisites

- Python 3.9 or higher
- Git (for cloning the repository)
- Virtual environment tool (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/esg-arcade.git
   cd esg-arcade
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Streamlit server**
   ```bash
   streamlit run app.py
   ```

2. **Access the application**
   Open your web browser and navigate to http://localhost:8501

### Using ESG Arcade

1. **Portfolio Map:** 
   - Explore your property portfolio on the interactive map
   - View top-performing properties by ESG score
   - Filter properties by type, location, or certification

2. **ESG Assessment:**
   - Select individual properties to view detailed ESG metrics
   - Compare property performance against portfolio averages
   - Identify specific areas for improvement

3. **Target Tracking:**
   - Monitor progress toward ESG targets 
   - Filter targets by category or priority
   - Track regulatory compliance deadlines

4. **Retrofit Simulator:**
   - Select properties for potential retrofits
   - Set budget constraints
   - Choose from available upgrade options
   - View projected improvements in ESG performance
   - Calculate ROI and implementation timelines

5. **ESG Reports:**
   - Generate standardized reports compatible with major frameworks
   - Export data in various formats
   - Share reports with stakeholders

### Customizing for Your Portfolio

To use the application with your own portfolio data:

1. Replace the sample data in `assets/sample_data/` with your property information
2. Customize the retrofit options in `assets/sample_data/retrofits.csv`
3. Adjust the target metrics in `modules/data_generator.py` if generating data programmatically

### Multi-Page Mode

For larger portfolios, you may prefer to use the multi-page mode:

```bash
# Run in multi-page mode
streamlit run pages/01_Portfolio_Map.py
```

This loads the application in Streamlit's multi-page mode, which can improve performance for complex portfolios.

## For the Common Good

Remember: Buildings, land, and resources ultimately belong to everyone. This tool helps ensure they are managed accordingly.

*"From each according to their ability, to each according to their needs."*
