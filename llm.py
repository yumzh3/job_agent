from dotenv import load_dotenv
import anthropic
import json
import csv
import os
from datetime import datetime

load_dotenv()                      # reads .env into environment variables
client = anthropic.Anthropic()     # finds ANTHROPIC_API_KEY automatically

PRICES = {  # USD per million tokens: (input, output)
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-sonnet-5-5": (2, 10),
    "claude-opus-5-5": (4, 20),
    "claude-fable-5-1": (10, 50),
}

def ask_json(prompt: str, schema: dict, system: str = "",
             model: str = "claude-haiku-5-5", max_tokens: int = 2048,
             purpose: str = "") -> dict:
    kwargs = dict(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
        output_config={
            "format": {
                "type": "json_schema",
                "schema": schema,
            }
        },
    )
    if system:
        kwargs["system"] = system
    response = client.messages.create(**kwargs)
    log_usage(purpose, model, response.usage)
    if response.stop_reason == "max_tokens":
        kwargs["max_tokens"] *= 2
        response = client.messages.create(**kwargs)
        log_usage(purpose, model, response.usage)
        if response.stop_reason == "max_tokens":
            raise RuntimeError(f"Output still cut off after retry ({purpose})")
    if response.stop_reason == "refusal":
        raise RuntimeError(f"Model refused ({purpose})")
    text = next(block.text for block in response.content if block.type == "text")
    return json.loads(text)

def log_usage(purpose, model, usage):
    log_file = "data/usage.csv"
    os.makedirs("data", exist_ok=True)
    write_header = not os.path.exists(log_file)
    with open(log_file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "purpose", "model", "in","out","cost"])
        if write_header:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "purpose": purpose,
            "model": model,
            "in": usage.input_tokens,
            "out": usage.output_tokens,
            "cost": usage.input_tokens/1_000_000 * PRICES.get(model, (0, 0))[0] + usage.output_tokens/1_000_000 * PRICES.get(model, (0, 0))[1],
        })

if __name__ == "__main__":
    job_post = """
Data Scientist (Senior Staff, Staff, & Senior roles available)
About the company
In the coming decades, demand for critical minerals such as copper, lithium, and cobalt will continue to grow. These minerals are needed to build electric infrastructure, vehicles, data centers, and electronics. However, the mining industry is making 10x fewer discoveries per dollar spent on exploration compared to 30 years ago because the easy-to-find, near surface deposits have largely been discovered.
KoBold was founded to be the first AI native mineral exploration, mine development, and technology development company. Our goal is to turn mineral exploration into a repeatable science to discover the minerals the world needs—by integrating artificial intelligence, human intelligence, and new technology. Our multidisciplinary teams of data scientists, engineers, and geologists work together to build data systems, design new sensors, and establish industry-leading workflows to develop and test subsurface predictions on our exploration projects.
Our first discovery, Mingomba, is a high-grade copper deposit in Zambia, found after spending materially less than industry average. We are developing Mingomba with the same technical rigor that we apply to exploration. The Mingomba team brings together mine and processing engineers, geologists, data scientists, software engineers, and community, health & safety, construction, and operations specialists. By combining industry knowledge and cutting edge technology, we are developing Mingomba into a world class project that has safer and more predictable outcomes for ourselves, partners, and communities. It is expected to create thousands of good jobs for generations.
KoBold runs exploration programs in eight countries, all with the potential for another discovery.
KoBold is privately held; investors include institutional asset managers T. Rowe Price and Canada Pension Plan Investments; technology venture capitalists Andreessen Horowitz, Breakthrough Energy Ventures, BOND Capital, Durable Capital, StepStone, and Standard Investments; and strategic natural resources companies BHP and Mitsubishi.
We are hiring a Data Scientists to help accelerate our mission.
About the position
In this role, you will build predictive models and apply a wide range of scientific computing, statistical, and physics-based methods to find places where there is evidence of ore-forming processes at work and to predict the locations of ore-grade mineralization in 2D and 3D. You will help build a worldwide dataset that underlies our exploration program, with careful attention to identifying and quantifying uncertainty in the data and in our predictions. You will create models and develop software to accelerate discovery of critical battery metals.
You will join an outstanding team of data scientists and engineers and will work closely with KoBold’s world-renowned geoscientists to incorporate our best understanding of the chemical and physical processes that create ore deposits. Working with your geoscience colleagues, you will create 2D and 3D geologic predictions, identify exploration targets, design field programs to collect data, and use that data to reduce the uncertainty in our predictions and guide the next phase of field work.
Ultimately, your role is to help KoBold make valuable discoveries by building data tools to solve scientific problems. As one of the early members of this team, you will help build these tools from the ground up.
Responsibilities
The Data Scientist will:
Help develop KoBold’s proprietary software exploration tools.
Find and curate  geophysical, geochemical, geologic, and geographic data and integrate it into KoBold’s proprietary data system.
Build models to make statistically valid predictions about the locations of compositional anomalies within the Earth’s crust.
Create effective visualizations for evaluating model performance and enabling rapid interaction with the underlying data and key features.
Develop and apply data processing, statistical, and physics-based techniques to geoscientific data — from computer vision to geophysical inversions — and use the results to guide our targeting efforts and inform our acquisition and exploration decisions.
Present to and collaborate with our external partners and stakeholders.
Qualifications
A great Data Scientist candidate will have:
Technical skills, including extensive experience with:
Python’s data science packages and general software engineering practices.
Collaborative software development (git), and familiarity with software engineering best practices like unit test / integration test suites, and CICD pipelines.
Cloud computing resources.
Building predictive models, applying them to different problems, and evaluating and interpreting the results.
Data from a variety of physical systems.
Geospatial analyses and visualizations.
Technical knowledge:
Broad skills in and knowledge of applied statistics and Bayesian inference
Substantial understanding of machine learning algorithms
Training and work experience:
An advanced degree in the physical sciences, engineering, computer science, or mathematics.
A minimum work experience of 4 years post PhD or 8 years post MS, ideally as a data scientist or data engineer. 
Experience leading technical teams to apply novel scientific approaches to core business problems 
Work practices and motivation:
Ability to take ownership and responsibility of large projects.
Ability to explain technical problems to and collaborate on solutions with domain experts.
Communicates well on a collaborative, cross-functional team. 
Excitement about joining a fast-growing early-stage company, comfort with a dynamic work environment, and eagerness to take on a range of responsibilities.
Ability to independently prioritize multiple tasks effectively.
Intellectual curiosity and eagerness to learn about all aspects of mineral exploration, particularly in the geology domain.
Enjoys constantly learning such that you are driving insights through using our tools in exploration and willing to work directly with geologists in the field.
Keen not just to build cool technology, but to figure out what technical product to build to best achieve the business objectives of the company.
A valid passport and willingness to travel to observe our work at Mingomba or at an exploration site around the world. 
It is also helpful but not required to have experience with:
Creating machine learning models on geospatial data
Geostatistics
Image processing or computer vision
Distributed computing applications for machine learning and other computations
"""
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "skills": {"type": "array", "items": {"type": "string"}},
            "seniority": {"type": "string", "enum": ["intern", "entry", "mid", "senior"]},
        },
        "required": ["title", "skills", "seniority"],
        "additionalProperties": False,
    }
    prompt = f"Extract info from this job post: {job_post}"
    result = ask_json(prompt, schema, purpose="test")
    print(result)