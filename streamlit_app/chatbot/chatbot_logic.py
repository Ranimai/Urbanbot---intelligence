# # Main Brain Controller
# # Orchestrator
# # DB → Report → Prompt → LLM → Answer

from chatbot.llm_client import generate_response
from chatbot.prompt import build_prompt
from chatbot.sql_agent import SQLAgent
from chatbot.email_agent import EmailAgent
from chatbot.report_agent import ReportAgent

# Create objects
agent = SQLAgent()
email_agent = EmailAgent()
report_agent = ReportAgent()

def chatbot_answer(question):

    question_lower = question.lower()
    context = None
    
    # ================= ACCIDENT =================

    if "accident" in question_lower:
        df = agent.fetch_dataframe(
            "SELECT city, severity, confidence_score, event_time FROM accident_events ORDER BY event_time DESC LIMIT 10"
        )

        if df.empty:
            return "⚠️ No accident data available in database."

        context = df.to_string(index=False)
        prompt = build_prompt(question, context)
        llm_output = generate_response(prompt)
        
        # Generate formatted report
        final_report = report_agent.generate_report(llm_output)

        # If user wants email
        if "email" in question_lower or "send" in question_lower:
            
            email_status = email_agent.send_email(
                "UrbanBot Accident Report",
                final_report
            )
            
            if email_status:
                return final_report + "\n\n📧 Report Emailed successfully."
            else:
                return final_report + "\n\n❌ Email failed. Check SMTP configuration."
                        
        return final_report

        
    # ================= TRAFFIC =================
    elif "traffic" in question_lower:
        df = agent.fetch_dataframe(
            "SELECT city, predicted_traffic, congestion_level, event_time FROM traffic_events ORDER BY event_time DESC LIMIT 5"
        )

        if df.empty:
            return "⚠️ No traffic data available in database."

        context = df.to_string(index=False)
        prompt = build_prompt(question, context)
        llm_output = generate_response(prompt)
        
        # Generate formatted report
        final_report = report_agent.generate_report(llm_output)

        # If user wants email
        if "email" in question_lower or "send" in question_lower:
            
            email_status = email_agent.send_email(
                "UrbanBot traffic Report",
                final_report
            )
            
            if email_status:
                return final_report + "\n\n📧 Report Emailed successfully."
            else:
                return final_report + "\n\n❌ Email failed. Check SMTP configuration."
                        
        return final_report
       
        
    # ================= AQI =================
    elif "aqi" in question_lower:
        df = agent.fetch_dataframe(
            "SELECT city, aqi, aqi_category, timestamp FROM air_quality_events ORDER BY timestamp DESC LIMIT 5"
        )

        if df.empty:
            return "⚠️ No AQI data available in database."

        context = df.to_string(index=False)
        prompt = build_prompt(question, context)
        llm_output = generate_response(prompt)
        
        # Generate formatted report
        final_report = report_agent.generate_report(llm_output)

        # If user wants email
        if "email" in question_lower or "send" in question_lower:
            
            email_status = email_agent.send_email(
                "UrbanBot AQI Report",
                final_report
            )
            
            if email_status:
                return final_report + "\n\n📧 Report Emailed successfully."
            else:
                return final_report + "\n\n❌ Email failed. Check SMTP configuration."
                        
        return final_report
    
    # ================= ROAD =================
    elif "road" in question_lower:
        df = agent.fetch_dataframe(
            "SELECT city, area, damage_count, event_time FROM road_damage_events ORDER BY event_time DESC LIMIT 5"
        )

        if df.empty:
            return "⚠️ No AQI data available in database."

        context = df.to_string(index=False)
        prompt = build_prompt(question, context)
        llm_output = generate_response(prompt)
        
        # Generate formatted report
        final_report = report_agent.generate_report(llm_output)

        # If user wants email
        if "email" in question_lower or "send" in question_lower:
            
            email_status = email_agent.send_email(
                "UrbanBot Road Damage Report",
                final_report
            )
            
            if email_status:
                return final_report + "\n\n📧 Report Emailed successfully."
            else:
                return final_report + "\n\n❌ Email failed. Check SMTP configuration."
                        
        return final_report
    
    # ================= CROWD =================
    elif "crowd" in question_lower:
        df = agent.fetch_dataframe(
            "SELECT city, camera_id, crowd_count, severity, event_time FROM crowd_events ORDER BY event_time DESC LIMIT 5"
        )

        if df.empty:
            return "⚠️ No AQI data available in database."

        context = df.to_string(index=False)
        prompt = build_prompt(question, context)
        llm_output = generate_response(prompt)
        
        # Generate formatted report
        final_report = report_agent.generate_report(llm_output)

        # If user wants email
        if "email" in question_lower or "send" in question_lower:
            
            email_status = email_agent.send_email(
                "UrbanBot Crowd Density Report",
                final_report
            )
            
            if email_status:
                return final_report + "\n\n📧 Report Emailed successfully."
            else:
                return final_report + "\n\n❌ Email failed. Check SMTP configuration."
                        
        return final_report
        
        
    # ================= COMPLAINTS =================
    elif "complaints" in question_lower:
        df = agent.fetch_dataframe(
            "SELECT city, category, sentiment, priority, created_at FROM nlp_complaints ORDER BY created_at DESC LIMIT 5"
        )

        if df.empty:
            return "⚠️ No AQI data available in database."

        context = df.to_string(index=False)
        prompt = build_prompt(question, context)
        llm_output = generate_response(prompt)
        
        # Generate formatted report
        final_report = report_agent.generate_report(llm_output)

        # If user wants email
        if "email" in question_lower or "send" in question_lower:
            
            email_status = email_agent.send_email(
                "UrbanBot Citizen Complaints Report",
                final_report
            )
            
            if email_status:
                return final_report + "\n\n📧 Report Emailed successfully."
            else:
                return final_report + "\n\n❌ Email failed. Check SMTP configuration."
                        
        return final_report

        
        
    # ================= GENERAL QUESTION =================
    else:
        return generate_response(question)

     # ===== Build prompt & generate response =====
    prompt = build_prompt(question, context)

    return generate_response(prompt)


