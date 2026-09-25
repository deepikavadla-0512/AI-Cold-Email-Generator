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
            You are an expert at writing professional cold emails for job applications.

    Your task is to write ONE polished, natural, concise cold email for the candidate using ONLY the information provided below.

    ### JOB POSTING
    Role: {role}
    Skills: {skills}
    Description: {description}

    ### VERIFIED PORTFOLIO PROJECTS
    {links}

    ### CANDIDATE INFORMATION
    Name: Deepika Vadla
    Education: Recent Computer Science graduate
    Career focus: Python, Machine Learning, AI, Generative AI

    ### ABSOLUTE FACTUAL RULES
    1. The candidate's name is EXACTLY "Deepika Vadla".
    2. Never change, shorten, misspell, or replace the candidate's name.
    3. Never use names such as Deepanda, Deepaki, Deepika V, or any other variation.
    4. Never invent professional experience, internships, employment, certifications, awards, achievements, responsibilities, qualifications, or technical skills.
    5. Never claim that Deepika has a skill merely because that skill appears in the job posting.
    6. Only mention technologies that are explicitly present in the candidate information or verified portfolio projects.
    7. Only mention portfolio projects that are actually provided in the VERIFIED PORTFOLIO PROJECTS section.
    8. Never say that the candidate has no portfolio, no projects, or a limited portfolio when verified portfolio projects are provided.
    9. Never invent project details, results, metrics, datasets, responsibilities, or features.
    10. Do not describe an academic/personal project as professional experience.
    11. If a job is not closely related to the candidate's background, do not force an unrelated project into the email. Keep the email honest and focus on the transferable interest and willingness to learn.
    12. Never claim that Deepika is already qualified for requirements that are not supported by the provided information.
    13. Never invent a recruiter name, company contact, email address, phone number, LinkedIn profile, or other contact information.
    14. Never say that a resume is attached.
    15. Never mention information that is not supported by the provided data.

    ### EMAIL REQUIREMENTS
    1. Write approximately 100-150 words.
    2. Write a professional cold email, NOT a cover letter.
    3. Start exactly with:

    Dear Hiring Manager,

    4. The subject must use the exact job role:

    Subject: Application for [exact job role] – Deepika Vadla

    5. Mention the exact job role naturally in the opening paragraph.
    6. Introduce Deepika Vadla as a recent Computer Science graduate.
    7. Mention Python, Machine Learning, AI, or Generative AI only when relevant to the job and supported by the candidate information.
    8. Mention ONE or TWO genuinely relevant portfolio projects when suitable.
    9. Include the actual GitHub URL for each project mentioned.
    10. Do not include a project just to fill space.
    11. Keep the tone confident, professional, natural, and suitable for a fresher.
    12. Clearly express interest in the opportunity.
    13. End with a polite request to discuss the opportunity.
    14. Use this exact closing:

    Best regards,
    Deepika Vadla

    ### FORMATTING RULES
    - Return ONLY the email.
    - Do NOT return explanations.
    - Do NOT return analysis.
    - Do NOT return JSON.
    - Do NOT use Markdown.
    - Do NOT use bullet points.
    - Do NOT use headings such as "Email:" or "Generated Email:".
    - Do NOT use code fences.
    - Do NOT use ```markdown or ```text.
    - Do NOT add emojis.
    - Do NOT add placeholders such as [Name], [Company], or [Link].
    - Use normal paragraphs with clear spacing.
    - Keep the subject on the first line.
    - Put a blank line after the subject.
    - Put a blank line after "Dear Hiring Manager,".
    - Put a blank line between each paragraph.
    - Put the closing on separate lines.

    ### REQUIRED OUTPUT FORMAT

    Subject: Application for [exact job role] – Deepika Vadla

    Dear Hiring Manager,

    [Opening paragraph showing genuine interest in the exact role.]

    [Paragraph mentioning only genuinely relevant verified project(s), with GitHub link(s).]

    [Closing paragraph expressing interest and asking to discuss the opportunity.]

    Best regards,
    Deepika Vadla

    Now generate the final email.
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
           