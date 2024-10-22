// Object yang berisi deskripsi pekerjaan berdasarkan value dari dropdown
const jobDescriptions = {
  ai_researcher: `We are a leading shipping and logistic company in Indonesia with forefront of AI innovation, dedicated to pushing the boundaries of technology. We seek a talented AI Researcher to join our team and contribute to cutting-edge projects.



Responsibilities:

Conduct data mining to uncover valuable insights and patterns.
Optimize AI systems for performance and scalability.
Collaborate with a multidisciplinary team to drive research initiatives.
Stay updated with the latest advancements in AI and machine learning.


Qualifications:

Advanced degree in Computer Science, Data Science, or a related field.
Proven experience in data mining and AI system optimization.
Strong programming skills in Python, R, or similar languages.
Excellent problem-solving and analytical abilities.
Willing to be placed in Surabaya.`,
  account_manager: `We are looking for someone who networks, makes connections, builds relationship, and pursues opportunities to join our commercial team. The ideal candidate will possess strong sales, interpersonal, and organizational skills. They should be comfortable to communicate with clients.



JOB DESCRIPTIONS:

Sell products and services to prospective customers
Maintain relationships with clients by providing support, information, and guidance
Prepare reports by collecting, analyzing, and summarizing information
Maintain quality service by establishing and enforcing organization standards


QUALIFICATIONS:

Candidate must possess at least Bachelor's Degree in any field Min. GPA 3.00
Fresh graduates are welcomed to apply
Willing to work hard and aggressive on the market
Punctual, good reporting, good in maintaining customers
Ability to communicate in Mandarin or other dialect would be an advantage
Willing to be placed in Tanjung Priok, North Jakarta with 6 months contract`,
  Senior_Customer_Service_Manager: `The National Customer Service Manager will be responsible for overseeing and enhancing the customer service experience across all our operations. This role requires a strategic thinker with excellent leadership skills, a deep understanding of the shipping and logistic industry, and strong expertise in business processes.



Qualifications:

Experience as Head of Customer Service.
Strong leadership and team management skills.
Excellent communication and interpersonal abilities.
Analytical mindset with the ability to interpret data and make data-driven decisions.
Proven experience in evaluating and improving business processes.
Willing to be placed in Jakarta or Surabaya`,
  senior_manager: `The Chief Strategy Officer will lead the company’s strategic planning initiatives, providing high-level expertise in market analysis, financial forecasting, mergers & acquisitions (M&A), and new business development. This role requires a seasoned professional with a background from a top-tier business consulting firm, along with extensive experience in financial analysis, market research, and P&L management. The CSO will work closely with the executive team to drive business growth, improve profitability, and identify new market opportunities.

  Key Responsibilities:
  
  Develop and execute strategic initiatives aligned with the company’s long-term vision and objectives.
  Conduct in-depth financial analysis, including financial projections, cash flow management, and profitability analysis, to support business decisions.
  Oversee and lead market research initiatives to identify emerging market trends, growth opportunities, and competitive threats.
  Develop feasibility studies to evaluate new business ventures, partnerships, and market entry strategies.
  Spearhead merger and acquisition (M&A) activities, including identifying potential targets, conducting due diligence, and overseeing integration strategies.
  Manage and oversee the company’s Profit & Loss (P&L), ensuring alignment with overall business goals and long-term financial health.
  Collaborate with the executive team to identify, evaluate, and pursue opportunities for new business development.
  Provide data-driven insights and recommendations to the CEO and senior leadership for strategic decision-making.
  Lead cross-functional teams in the implementation of key strategic projects, ensuring alignment across all departments.
  Establish and manage KPIs to monitor the success of strategic initiatives and their impact on the business.
  Foster strategic partnerships and alliances to support business growth and market expansion.
  
  Qualifications:
  
  MBA or advanced degree in Business, Finance, Economics, or a related field from a top-tier university.
  10+ years of experience in strategy and business development roles, with significant time spent at a leading business consulting firm (e.g., McKinsey, BCG, Bain, etc.).
  Extensive experience in financial analysis, financial projections, and market research.
  Proven experience in mergers and acquisitions (M&A), including deal structuring, due diligence, and post-merger integration.
  Strong expertise in profit and loss (P&L) management, with a track record of improving business profitability.
  Demonstrated success in new business development, including identifying and capitalizing on market opportunities.
  Exceptional analytical and problem-solving skills, with the ability to translate data into actionable insights.
  Strong leadership skills with the ability to work cross-functionally and manage multiple stakeholders.
  Excellent communication, negotiation, and presentation skills.
  
  Preferred Skills:
  
  Experience in a fast-paced, growth-oriented industry.
  Background in corporate finance or investment banking.
  Knowledge of global market trends and competitive landscapes`,
  magang : `AI Rudder is a software company that harnesses the power of AI voice automation to supercharge customer experiences. With AI voice assistants, your call center can make quality human-like calls at lightning speeds, collecting and analyzing data automatically to reach and activate more customers. AI Rudder helps call centers reduce costs by automating repetitive tasks and lowering agent workload. This frees up agents to focus on things only humans can do. Over the long term, AI Rudder aims to rethink the future of business communication.

Sell the next wave of highly demanded solutions.



Job Description:

Hiring careful and skilled Freelance NLP Annotators (Melayu Malaysia Speaker) to help annotate text data to improve Natural Language Processing (NLP) models.



About the Job

1. Accurately annotate text data based on standard procedures;

2. Ensure quality and accuracy of annotations in various NLP aspects;

3. Complete projects on time while still maintaining high accuracy;

4. Give feedback if there are problems or unclear tasks;

5. The support team needs to complete projects successfully.



Who you are:

1. Preferably top university, not limited the majors, bachelor’s degree or above (min. 3rd semester) ;

2. Ability to follow instructions;

3. Attention to detail and commitment to accuracy;

4. Good problem-solving skills.

5. Good English communication skills (point plus if you know Mandarin).

6. At least 3 days/week, the internship period is minimal 3 months, long-term interns are preferred.

AI Rudder is an Equal Opportunity Employer. We’re committed to building a diverse and inclusive team. We do not discriminate against qualified employees or applicants.

 

We regret that only shortlisted candidates will be contacted.

Qualifications
7 of 9 skills match your profile - you may be a good fit
Requirements added by the job poster
Can start immediately
Working in an onsite setting
1+ years of work experience with Natural Language Processing (NLP)`,
  satpam : `Memastikan keamanan dan ketertiban lingkungan kerja untuk menunjang kelancaran operasional kegiatan perusahaan.
Menerapkan dan mengawasi pelaksanaan Standard Operation Procedure (SOP).
Melakukan pengawasan terhadap pelaksanaan tugas-tugas pengamanan.
Memberikan laporan secara berkala mengenai pelaksanaan tugas-tugas Pengamanan.
Syarat:

Pendidikan minimal SMA/SMU/SMK sederajat
Lulus tes kesehatan dan kesamaptaan
Pengalaman minimal 1 tahun
Berpenampilan rapi, baik dan sopan
Menyertakan Surat Keterangan Catatan Kepolisian (SKCK)
Usia minimal 20 tahun dan maksimal 35 tahun
Wajib lulus diklat satpam, memiliki KTA dan sertifikat dari Polda setempat (Gada Pratama untuk Secpri) atau (Gada Madya untuk Komandan Regu)`
};

// Menangani perubahan pilihan pada dropdown
document.getElementById("job-position").addEventListener("change", function () {
  const selectedValue = this.value;
  const jobDescription = jobDescriptions[selectedValue];

  // Menampilkan textarea dan mengisi dengan deskripsi pekerjaan
  const textarea = document.getElementById("job_description");
  textarea.value = jobDescription || "No description available";
});

// Event listener for the file input to display the selected file name
document.getElementById("resume").addEventListener("change", function () {
  var fileInput = document.getElementById("resume");
  if (fileInput.files.length > 0) {
    var fileName = fileInput.files[0].name;
    document.getElementById("file-name").textContent =
      "Selected file: " + fileName;
  } else {
    document.getElementById("file-name").textContent = "";
  }
});

// Event listener for form submission
document
  .getElementById("cv-upload-form")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default form submission

    var submitButton = document.getElementById("submitcv-btn");
    var spinner = document.getElementById("spinner-cv");
    var status = document.getElementById("upload-status");
    var formData = new FormData(this); // Create a FormData object

    // Reset status message on form submit
    status.innerHTML = "";

    // Tampilkan spinner dan nonaktifkan tombol submit
    spinner.style.display = "inline-block";
    submitButton.disabled = true;

    // Send the form data using fetch API
    fetch("/process-uploaded_cv", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((err) => {
            throw new Error(err.botResponse);
          });
        }
        return response.json(); // Parse JSON response
      })
      .then((data) => {
        // Hide spinner and enable button after completion
        spinner.style.display = "none";
        submitButton.disabled = false;

        // Handle success
        console.log(data);
        status.innerHTML = "<p style='color: green;'>CV berhasil diupload!</p>";
      })
      .catch((error) => {
        console.error("There was a problem with the fetch operation:", error);

        // Hide spinner and enable button after error
        spinner.style.display = "none";
        submitButton.disabled = false;

        // Show error message
        status.innerHTML =
          "<p style='color: red;'>Error uploading CV: " +
          error.message +
          "</p>";
      });
  });

// Event listener for ranking applicants button
document
  .getElementById("rank-applicants-btn")
  .addEventListener("click", function () {
    var spinner = document.getElementById("spinner");
    spinner.style.display = "inline-block"; // Show spinner
    this.disabled = true; // Disable the button

    var jobDescription = document.querySelector(
      'textarea[name="job_description"]'
    ).value;

    fetch("/rank-applicants", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ job_description: jobDescription }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error in ranking applicants");
        }
        return response.json(); // Parse JSON response
      })
      .then((data) => {
        // Handle success and display ranking results as HTML
        console.log(data);
        document.getElementById("ranking-results").innerHTML = data.response; // Use innerHTML for HTML content
        spinner.style.display = "none";
        this.disabled = false;
        // alert("Ranking completed successfully!");
      })
      .catch((error) => {
        console.error("There was a problem with the fetch operation:", error);
        // alert("Error ranking applicants: " + error.message);
      });
  });
