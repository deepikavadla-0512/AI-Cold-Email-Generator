import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="openai/gpt-oss-120b"
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            Extract job postings from the above text.

            Return a JSON object with a key "jobs".
            Each job should contain:
            - role
            - skills
            - description

            Return only valid JSON.
            """
        )

        chain_extract = prompt_extract | self.llm | JsonOutputParser()

        try:
            res = chain_extract.invoke({"page_data": cleaned_text})
            return res.get("jobs", [])
        except OutputParserException:
            raise OutputParserException("Unable to extract jobs from the page.")

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            You are writing a real cold email for a recent Computer Science graduate.

            ### JOB POSTING:
            Role: {role}
            Skills: {skills}
            Description: {description}

            ### PORTFOLIO:
            {links}

            ### CANDIDATE:
            Name: Deepika Vadla
            Status: Recent Computer Science graduate
            Interests: Python, Machine Learning, AI, Generative AI

            ### STRICT RULES:
            1. Write approximately 100-150 words.
            2. Write a cold email, NOT a cover letter.
            3. Start with "Dear Hiring Manager,".
            4. Introduce Deepika Vadla as a recent Computer Science graduate.
            5. Mention the exact job role.
            6. Mention only 1 or 2 relevant portfolio projects.
            7. Use ONLY technologies present in the portfolio.
            8. Describe projects only using the information provided in the portfolio.
            9. Include the relevant GitHub link(s).
            10. Never invent experience, internships, achievements, certifications,
                responsibilities, metrics, percentages, technologies or qualifications.
            11. Do not claim professional experience.
            12. Do not turn job requirements into claims about Deepika.
            13. Do not invent recruiter names, company details, email addresses,
                phone numbers or LinkedIn URLs.
            14. Do not say that a resume is attached.
            15. Do not use Markdown bullets.
            16. Do not use Markdown formatting.
            17. Return ONLY the final email.

            ### EMAIL STRUCTURE:

            Subject: Application for [Job Role] – Deepika Vadla

            Dear Hiring Manager,

            Brief introduction and interest in the specific role.

            Mention 1-2 relevant projects with factual descriptions and GitHub links.

            Briefly express interest in the opportunity and willingness to learn.

            Ask whether the opportunity can be discussed.

            Best regards,
            Deepika Vadla
            """
        )

        chain_email = prompt_email | self.llm

        res = chain_email.invoke(
            {
                "role": job.get("role", ""),
                "skills": ", ".join(job.get("skills", [])),
                "description": job.get("description", ""),
                "links": str(links)
            }
        )

        return res.content.strip()
           