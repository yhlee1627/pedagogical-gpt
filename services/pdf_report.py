from fpdf import FPDF
import os

def generate_pdf_report(student_id, conversation_id, evaluation_data):
    os.makedirs("data/evaluation_logs", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()

    # ✅ 폰트 경로
    font_folder = "services"
    regular_font_path = os.path.join(font_folder, "NanumGothic-Regular.ttf")
    bold_font_path = os.path.join(font_folder, "NanumGothic-Bold.ttf")

    # ✅ 폰트 등록 + 예외 처리
    font_loaded = False
    try:
        pdf.add_font("Nanum", "", regular_font_path, uni=True)
        pdf.add_font("Nanum", "B", bold_font_path, uni=True)
        font_loaded = True
    except Exception as e:
        print("⚠️ 한글 폰트 등록 실패:", e)

    # ✅ 제목
    if font_loaded:
        pdf.set_font("Nanum", "B", size=14)
    else:
        pdf.set_font("Arial", "B", size=14)
    pdf.cell(200, 10, txt="GPT 평가 리포트", ln=True, align='C')
    pdf.ln(10)

    # ✅ 기본 정보
    if font_loaded:
        pdf.set_font("Nanum", "", size=12)
    else:
        pdf.set_font("Arial", "", size=12)

    pdf.cell(200, 10, txt=f"학생: {student_id}", ln=True)
    pdf.cell(200, 10, txt=f"대화 ID: {conversation_id}", ln=True)
    pdf.ln(5)

    # ✅ 평가 결과 출력
    scores = evaluation_data.get("scores", {})
    explanations = evaluation_data.get("explanations", {})
    summary = evaluation_data.get("summary", "")

    if font_loaded:
        pdf.set_font("Nanum", "B", size=12)
    else:
        pdf.set_font("Arial", "B", size=12)

    pdf.cell(200, 10, txt="📊 평가 항목별 점수 및 설명", ln=True)
    pdf.ln(5)

    if font_loaded:
        pdf.set_font("Nanum", "", size=11)
    else:
        pdf.set_font("Arial", "", size=11)

    for criterion, score in scores.items():
        explanation = explanations.get(criterion, "")
        pdf.cell(200, 8, txt=f"- {criterion}: {score}점", ln=True)
        if explanation:
            pdf.multi_cell(0, 8, txt=f"  설명: {explanation}")

    pdf.ln(5)
    if font_loaded:
        pdf.set_font("Nanum", "B", size=12)
    else:
        pdf.set_font("Arial", "B", size=12)

    pdf.cell(200, 10, txt="📝 총평", ln=True)

    if font_loaded:
        pdf.set_font("Nanum", "", size=11)
    else:
        pdf.set_font("Arial", "", size=11)

    pdf.multi_cell(0, 8, txt=summary)

    # ✅ 저장
    output_path = f"data/evaluation_logs/{conversation_id}_report.pdf"
    pdf.output(output_path)
    return output_path