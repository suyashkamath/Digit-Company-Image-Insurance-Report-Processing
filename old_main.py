# # # from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# # # from fastapi.responses import JSONResponse, HTMLResponse
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from io import BytesIO
# # # import base64
# # # import json
# # # import os
# # # from dotenv import load_dotenv
# # # import logging
# # # import re
# # # import pandas as pd
# # # from openai import OpenAI
# # # from pathlib import Path

# # # # Configure logging
# # # logging.basicConfig(
# # #     level=logging.INFO,
# # #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# # # )
# # # logger = logging.getLogger(__name__)

# # # # Load environment variables
# # # load_dotenv()

# # # # Load OpenAI API key
# # # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# # # if not OPENAI_API_KEY:
# # #     logger.error("⚠️ OPENAI_API_KEY environment variable not set")
# # #     raise RuntimeError("OPENAI_API_KEY environment variable not set. Please create a .env file with OPENAI_API_KEY=your-key")

# # # # Initialize OpenAI client
# # # try:
# # #     client = OpenAI(api_key=OPENAI_API_KEY)
# # #     logger.info("✅ OpenAI client initialized successfully")
# # # except Exception as e:
# # #     logger.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
# # #     raise RuntimeError(f"Failed to initialize OpenAI client: {str(e)}")

# # # app = FastAPI(title="Insurance Policy Processing System")

# # # # Add CORS middleware for frontend compatibility
# # # # Add CORS middleware for frontend compatibility
# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"],  # <-- allow all origins in development (use specific origins in production)
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )
# # # # Embedded Formula Data
# # # FORMULA_DATA = [
# # #     {"LOB": "TW", "SEGMENT": "1+5", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "NIL"},
# # #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "NIL"},
# # #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# # #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
# # #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
# # #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-5%", "REMARKS": "Payin Above 50%"},
# # #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Bajaj, Digit, ICICI", "PO": "-3%", "REMARKS": "Payin Above 20%"},
# # #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# # #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
# # #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
# # #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
# # #     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR COMP + SAOD", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "All Fuel"},
# # #     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Bajaj, Digit, SBI", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# # #     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Bajaj, Digit, SBI", "PO": "-3%", "REMARKS": "Payin Above 20%"},
# # #     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Rest of Companies", "PO": "90% of Payin", "REMARKS": "Zuno - 21"},
# # #     {"LOB": "CV", "SEGMENT": "Upto 2.5 GVW", "INSURER": "Reliance, SBI", "PO": "-2%", "REMARKS": "NIL"},
# # #     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# # #     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
# # #     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
# # #     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
# # #     {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "INSURER": "TATA, Reliance, Digit, ICICI", "PO": "Less 2% of Payin", "REMARKS": "NIL"},
# # #     {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "INSURER": "Rest of Companies", "PO": "88% of Payin", "REMARKS": "NIL"},
# # #     {"LOB": "BUS", "SEGMENT": "STAFF BUS", "INSURER": "All Companies", "PO": "88% of Payin", "REMARKS": "NIL"},
# # #     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# # #     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
# # #     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
# # #     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
# # #     {"LOB": "MISD", "SEGMENT": "Misd, Tractor", "INSURER": "All Companies", "PO": "88% of Payin", "REMARKS": "NIL"}
# # # ]

# # # def extract_text_from_file(file_bytes: bytes, filename: str, content_type: str) -> str:
# # #     """Extract text from uploaded image file using OCR with enhanced prompting"""
# # #     file_extension = filename.split('.')[-1].lower() if '.' in filename else ''
# # #     file_type = content_type if content_type else file_extension

# # #     # Image-based extraction with enhanced OCR
# # #     image_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
# # #     if file_extension in image_extensions or file_type.startswith('image/'):
# # #         try:
# # #             image_base64 = base64.b64encode(file_bytes).decode('utf-8')
            
# # #             prompt = """Extract ALL text from this insurance policy image with extreme accuracy.

# # # CRITICAL INSTRUCTIONS:
# # # 1. Read EVERY piece of text visible in the image, including:
# # #    - Headers, titles, and section names
# # #    - All table data (columns and rows)
# # #    - Segment/LOB information (TW, PVT CAR, CV, BUS, TAXI, MISD)
# # #    - Company names
# # #    - Policy types (TP, COMP, SAOD, etc.)
# # #    - Payin/Payout percentages or decimals
# # #    - Weight/tonnage (e.g., "upto 2.5 Tn", "2.5 GVW")
# # #    - Vehicle makes (Tata, Maruti, etc.)
# # #    - Age information (>5 years, etc.)
# # #    - Transaction types (New, Old, Renewal)
# # #    - Location/district information
# # #    - Validity dates
# # #    - ALL numerical values
# # #    - Any remarks, notes, or conditions

# # # 2. Preserve the EXACT format and structure of tables if present
# # # 3. If there's a table, clearly indicate column headers and separate rows
# # # 4. For numbers that look like decimals (0.625, 0.34), preserve them exactly
# # # 5. For percentages (34%, 62.5%), preserve them exactly
# # # 6. Extract text in a structured, organized manner

# # # Extract all insurance policy text accurately from this image using OCR.
# # #         Pay special attention to identifying:
# # #         - Agency/PB Clusters (these are locations)
# # #         - Agency/PB segments (these are vehicle segments, e.g., SC/EV, MC, TW 1+5)
# # #         - CD2 values (these are payin percentages - IGNORE CD1 completely)
# # #         - Policy codes like 1+1, 1+3, 1+5, SATP, TP
# # #         - Company names
# # #         - Any percentage values
# # #         - Any numerical data
# # #         - Table structure, including if values are NIL under certain columns
# # #         - If CD1 columns exist, ignore them completely, only extract CD2 values
# # #         - If 1+1 CD2 (COMP) is NIL but SATP CD2 (TP) has a value, note this relationship
# # #         Extract all text exactly as it appears in the image.

# # # Return the complete text extraction - do not summarize or skip anything."""
                
# # #             response = client.chat.completions.create(
# # #                 model="gpt-4o",
# # #                 messages=[{
# # #                     "role": "user",
# # #                     "content": [
# # #                         {"type": "text", "text": prompt},
# # #                         {"type": "image_url", "image_url": {"url": f"data:image/{file_extension};base64,{image_base64}"}}
# # #                     ]
# # #                 }],
# # #                 temperature=0.0,
# # #                 max_tokens=4000
# # #             )
            
# # #             extracted_text = response.choices[0].message.content.strip()
            
# # #             if not extracted_text or len(extracted_text) < 10:
# # #                 logger.error("OCR returned very short or empty text")
# # #                 return ""
            
# # #             return extracted_text
            
# # #         except Exception as e:
# # #             logger.error(f"Error in OCR extraction: {str(e)}")
# # #             raise ValueError(f"Failed to extract text from image: {str(e)}")

# # #     raise ValueError(f"Unsupported file type for {filename}. Only images are supported.")

# # # def clean_json_response(response_text: str) -> str:
# # #     """Clean and extract valid JSON array from OpenAI response"""
# # #     cleaned = re.sub(r'```json\s*|\s*```', '', response_text).strip()
    
# # #     start_idx = cleaned.find('[')
# # #     end_idx = cleaned.rfind(']') + 1 if cleaned.rfind(']') != -1 else len(cleaned)
    
# # #     if start_idx != -1 and end_idx > start_idx:
# # #         cleaned = cleaned[start_idx:end_idx]
# # #     else:
# # #         logger.warning("No valid JSON array found in response, returning empty array")
# # #         return "[]"
    
# # #     if not cleaned.startswith('['):
# # #         cleaned = '[' + cleaned
# # #     if not cleaned.endswith(']'):
# # #         cleaned += ']'
    
# # #     return cleaned

# # # def ensure_list_format(data) -> list:
# # #     """Ensure data is in list format"""
# # #     if isinstance(data, list):
# # #         return data
# # #     elif isinstance(data, dict):
# # #         return [data]
# # #     else:
# # #         raise ValueError(f"Expected list or dict, got {type(data)}")

# # # def classify_payin(payin_str):
# # #     """Converts Payin string to float and classifies its range"""
# # #     try:
# # #         payin_clean = str(payin_str).replace('%', '').replace(' ', '').strip()
        
# # #         if not payin_clean or payin_clean.upper() == 'N/A':
# # #             return 0.0, "Payin Below 20%"
        
# # #         payin_value = float(payin_clean)
        
# # #         if payin_value <= 20:
# # #             category = "Payin Below 20%"
# # #         elif 21 <= payin_value <= 30:
# # #             category = "Payin 21% to 30%"
# # #         elif 31 <= payin_value <= 50:
# # #             category = "Payin 31% to 50%"
# # #         else:
# # #             category = "Payin Above 50%"
# # #         return payin_value, category
# # #     except (ValueError, TypeError) as e:
# # #         logger.warning(f"Could not parse payin value: {payin_str}, error: {e}")
# # #         return 0.0, "Payin Below 20%"

# # # def apply_formula_directly(policy_data, company_name):
# # #     """Apply formula rules directly using Python logic with default STAFF BUS for unspecified BUS"""
# # #     if not policy_data:
# # #         logger.warning("No policy data to process")
# # #         return []
    
# # #     calculated_data = []
    
# # #     for record in policy_data:
# # #         try:
# # #             segment = str(record.get('Segment', '')).upper()
# # #             payin_value = record.get('Payin_Value', 0)
# # #             payin_category = record.get('Payin_Category', '')
            
# # #             lob = ""
# # #             segment_upper = segment.upper()
            
# # #             if any(tw_keyword in segment_upper for tw_keyword in ['TW', '2W', 'TWO WHEELER', 'TWO-WHEELER']):
# # #                 lob = "TW"
# # #             elif any(car_keyword in segment_upper for car_keyword in ['PVT CAR', 'PRIVATE CAR', 'CAR', 'PCI']):
# # #                 lob = "PVT CAR"
# # #             elif any(cv_keyword in segment_upper for cv_keyword in ['CV', 'COMMERCIAL', 'LCV', 'GVW', 'TN', 'UPTO', 'ALL GVW', 'PCV', 'GCV']):
# # #                 lob = "CV"
# # #             elif 'BUS' in segment_upper:
# # #                 lob = "BUS"
# # #             elif 'TAXI' in segment_upper:
# # #                 lob = "TAXI"
# # #             elif any(misd_keyword in segment_upper for misd_keyword in ['MISD', 'TRACTOR', 'MISC', 'AMBULANCE', 'POLICE VAN', 'GARBAGE VAN']):
# # #                 lob = "MISD"
# # #             else:
# # #                 remarks_upper = str(record.get('Remarks', '')).upper()
# # #                 if any(cv_keyword in remarks_upper for cv_keyword in ['TATA', 'MARUTI', 'GVW', 'TN']):
# # #                     lob = "CV"
# # #                 else:
# # #                     lob = "UNKNOWN" 
            
# # #             matched_segment = segment_upper
# # #             if lob == "BUS":
# # #                 if "SCHOOL" not in segment_upper and "STAFF" not in segment_upper:
# # #                     matched_segment = "STAFF BUS"
# # #                 elif "SCHOOL" in segment_upper:
# # #                     matched_segment = "SCHOOL BUS"
# # #                 elif "STAFF" in segment_upper:
# # #                     matched_segment = "STAFF BUS"
            
# # #             matched_rule = None
# # #             rule_explanation = ""
# # #             company_normalized = company_name.upper().replace('GENERAL', '').replace('INSURANCE', '').strip()
            
# # #             for rule in FORMULA_DATA:
# # #                 if rule["LOB"] != lob:
# # #                     continue
                    
# # #                 rule_segment = rule["SEGMENT"].upper()
# # #                 segment_match = False
                
# # #                 if lob == "CV":
# # #                     if "UPTO 2.5" in rule_segment:
# # #                         if any(keyword in segment_upper for keyword in ["UPTO 2.5", "2.5 TN", "2.5 GVW", "2.5TN", "2.5GVW", "UPTO2.5"]):
# # #                             segment_match = True
# # #                     elif "ALL GVW" in rule_segment:
# # #                         segment_match = True
# # #                 elif lob == "BUS":
# # #                     if matched_segment == rule_segment:
# # #                         segment_match = True
# # #                 elif lob == "PVT CAR":
# # #                     if "COMP" in rule_segment and any(keyword in segment for keyword in ["COMP", "COMPREHENSIVE", "PACKAGE", "1ST PARTY", "1+1"]):
# # #                         segment_match = True
# # #                     elif "TP" in rule_segment and "TP" in segment and "COMP" not in segment:
# # #                         segment_match = True
# # #                 elif lob == "TW":
# # #                     if "1+5" in rule_segment and any(keyword in segment for keyword in ["1+5", "NEW", "FRESH"]):
# # #                         segment_match = True
# # #                     elif "SAOD + COMP" in rule_segment and any(keyword in segment for keyword in ["SAOD", "COMP", "PACKAGE", "1ST PARTY", "1+1"]):
# # #                         segment_match = True
# # #                     elif "TP" in rule_segment and "TP" in segment:
# # #                         segment_match = True
# # #                 else:
# # #                     segment_match = True
                
# # #                 if not segment_match:
# # #                     continue
                
# # #                 insurers = [ins.strip().upper() for ins in rule["INSURER"].split(',')]
# # #                 company_match = False
                
# # #                 if "ALL COMPANIES" in insurers:
# # #                     company_match = True
# # #                 elif "REST OF COMPANIES" in insurers:
# # #                     is_in_specific_list = False
# # #                     for other_rule in FORMULA_DATA:
# # #                         if (other_rule["LOB"] == rule["LOB"] and 
# # #                             other_rule["SEGMENT"] == rule["SEGMENT"] and
# # #                             "REST OF COMPANIES" not in other_rule["INSURER"] and
# # #                             "ALL COMPANIES" not in other_rule["INSURER"]):
# # #                             other_insurers = [ins.strip().upper() for ins in other_rule["INSURER"].split(',')]
# # #                             if any(company_key in company_normalized for company_key in other_insurers):
# # #                                 is_in_specific_list = True
# # #                                 break
# # #                     if not is_in_specific_list:
# # #                         company_match = True
# # #                 else:
# # #                     for insurer in insurers:
# # #                         if insurer in company_normalized or company_normalized in insurer:
# # #                             company_match = True
# # #                             break
                
# # #                 if not company_match:
# # #                     continue
                
# # #                 remarks = rule.get("REMARKS", "")
                
# # #                 if remarks == "NIL" or "NIL" in remarks.upper():
# # #                     matched_rule = rule
# # #                     rule_explanation = f"Direct match: LOB={lob}, Segment={rule_segment}, Company={rule['INSURER']}"
# # #                     break
# # #                 elif any(payin_keyword in remarks for payin_keyword in ["Payin Below", "Payin 21%", "Payin 31%", "Payin Above"]):
# # #                     if payin_category in remarks:
# # #                         matched_rule = rule
# # #                         rule_explanation = f"Payin category match: LOB={lob}, Segment={rule_segment}, Payin={payin_category}"
# # #                         break
# # #                 else:
# # #                     matched_rule = rule
# # #                     rule_explanation = f"Other remarks match: LOB={lob}, Segment={rule_segment}, Remarks={remarks}"
# # #                     break
            
# # #             if matched_rule:
# # #                 po_formula = matched_rule["PO"]
# # #                 calculated_payout = payin_value
                
# # #                 if "90% of Payin" in po_formula:
# # #                     calculated_payout *= 0.9
# # #                 elif "88% of Payin" in po_formula:
# # #                     calculated_payout *= 0.88
# # #                 elif "Less 2% of Payin" in po_formula:
# # #                     calculated_payout -= 2
# # #                 elif "-2%" in po_formula:
# # #                     calculated_payout -= 2
# # #                 elif "-3%" in po_formula:
# # #                     calculated_payout -= 3
# # #                 elif "-4%" in po_formula:
# # #                     calculated_payout -= 4
# # #                 elif "-5%" in po_formula:
# # #                     calculated_payout -= 5
                
# # #                 calculated_payout = max(0, calculated_payout)
# # #                 formula_used = po_formula
# # #             else:
# # #                 calculated_payout = payin_value
# # #                 formula_used = "No matching rule found"
            
# # #             result_record = record.copy()
# # #             result_record['Calculated Payout'] = f"{calculated_payout:.2f}%"
# # #             result_record['Formula Used'] = formula_used
# # #             result_record['Rule Explanation'] = rule_explanation
            
# # #             calculated_data.append(result_record)
            
# # #         except Exception as e:
# # #             logger.error(f"Error processing record: {record}, error: {str(e)}")
# # #             result_record = record.copy()
# # #             result_record['Calculated Payout'] = "Error"
# # #             result_record['Formula Used'] = "Error in calculation"
# # #             result_record['Rule Explanation'] = f"Error: {str(e)}"
# # #             calculated_data.append(result_record)
    
# # #     return calculated_data

# # # def process_files(policy_file_bytes: bytes, policy_filename: str, policy_content_type: str, company_name: str):
# # #     """Main processing function with enhanced error handling"""
# # #     try:
# # #         logger.info("=" * 50)
# # #         logger.info(f"🚀 Starting file processing for {policy_filename}...")
# # #         logger.info(f"📁 File size: {len(policy_file_bytes)} bytes")
        
# # #         # Extract text
# # #         logger.info("🔍 Extracting text from policy image...")
# # #         extracted_text = extract_text_from_file(policy_file_bytes, policy_filename, policy_content_type)
# # #         logger.info(f"✅ Extracted text length: {len(extracted_text)} chars")

# # #         if not extracted_text.strip():
# # #             logger.error("No text extracted from the image")
# # #             raise ValueError("No text could be extracted. Please ensure the image is clear and contains readable text.")

# # #         # Parse with AI
# # #         logger.info("🧠 Parsing policy data with AI...")
        
# # #         parse_prompt="""
# # #     Analyze this insurance policy text and extract structured data.



# # # CRITICAL INSTRUCTIONS:
# # # 1. ALWAYS return a valid JSON ARRAY (list) of objects, even if there's only one record or no data is found. If multiple lines, tables, emails, or messages are present (e.g., grids with rows, forwarded messages), create a separate object for each row or entry.
# # # 2. Each object must have these EXACT field names:
# # #    - "Segment": Standardized LOB + policy type (e.g., "TW TP", "PVT CAR COMP + SAOD", "Upto 2.5 GVW"). If unsure or no data, use "Unknown".
# # #    - "Location": location/region information (e.g., "Mumbai, Pune", "Nagpur", "RTO Cluster: GOA", states like "GA", "JH", RTOs like "R13", "MP1, MP2", use "N/A" if not found).
# # #    - "Policy Type": policy type details (use "N/A" if not specified, or "COMP/TP" if mixed, "SATP" maps to "TP").
# # #    - "Payin": percentage value (convert decimals: 0.625 → 62.5%, or keep as is: 34%, use "0%" if not found; extract petrol/diesel separately if present).
# # #    - "Doable District": district info or RTO-related (use "N/A" if not found).
# # #    - "Remarks": additional info including vehicle makes, age (e.g., ">6 years"), transaction type, validity, fuel type (e.g., "Petrol: 50%, Diesel: 45%"), notes (e.g., "Decrease by 3%", "No additional deal", "irrespective of Institution"), month/year (e.g., "June 25", "FY 25-26"), and raw text snippets if ambiguous.

# # # 3. For Segment field:
# # #    - First, identify the LOB: TW (Two Wheeler, including MCY for motorcycles or scooters), PVT CAR (Private Car or PCI), CV (Commercial Vehicle), BUS, TAXI, MISD (Miscellaneous).
# # #    - Then, determine policy type: TP (Third Party, including SATP), COMP (Comprehensive, or synonyms like package, 1st party, 1+1), SAOD (Stand Alone Own Damage), etc.
# # #    - Use your intelligence to standardize the "Segment" to EXACTLY match one of these predefined values based on the text content, keywords, tonnage, or descriptions. If no match or unclear, use "Unknown":
# # #      - TW-related (including MCY for motorcycles/scooters):
# # #        - If mentions 1+5 year plan, long-term policy, new, or fresh: "1+5"
# # #        - If SAOD + COMP, Comprehensive + Own Damage, package, 1st party, 1+1, or similar full coverage: "TW SAOD + COMP"
# # #        - If TP only, Third Party, or liability-only (including SATP): "TW TP"
# # #      - PVT CAR-related (or PCI):
# # #        - If COMP + SAOD, Comprehensive + Own Damage, package, 1st party, 1+1, or full coverage: "PVT CAR COMP + SAOD"
# # #        - If TP only or Third Party (including SATP): "PVT CAR TP"
# # #      - CV-related (Commercial Vehicle):
# # #        - If upto 2.5 Tn, 2.5 GVW, or similar low tonnage/weight (e.g., "upto 2.5", "2.5 Tn"): "Upto 2.5 GVW"
# # #        - For all other CV cases, higher tonnage (e.g., "2.5 - 3.5 Tn", "3.5-12 Tn", ">3.5-45 Tn", "12-45 Tn"), PCV 3W, GCV 3W, or general CV: "All GVW & PCV 3W, GCV 3W"
# # #      - BUS-related:
# # #        - If School Bus or educational (e.g., "School bus >14 seater", "<11 SC"): "SCHOOL BUS"
# # #        - If Staff Bus, corporate, or other bus types: "STAFF BUS"
# # #      - TAXI-related: "TAXI"
# # #      - MISD-related (Miscellaneous, Tractor, ambulance, police van, garbage van, etc.): "Misd, Tractor"
# # #    - If ambiguous, infer from context (e.g., tonnage for CV, "Private Car SATP" to "PVT CAR TP") and default to "Unknown".

# # # 4. For Payin field:
# # #    - If you see decimals like 0.625, convert to 62.5%
# # #    - If you see whole numbers like 34, add % to make 34%
# # #    - If you see percentages, keep them as is (e.g., "50%", "45%", " -72%")
# # #    - Use the value from the "PO" column, "Payin" column, or any percentage in grids (e.g., Petrol/Diesel columns, or "2.5%").
# # #    - If multiple (e.g., Petrol and Diesel), use "Petrol: X%, Diesel: Y%" in Payin or move to Remarks.
# # #    - If not found, use "0%"
# # #    - Do not use values from "Discount" column

# # # 5. For Remarks field - extract ALL additional info:
# # #    - Vehicle makes (Tata, Maruti, etc.) → "Vehicle Makes: Tata, Maruti"
# # #    - Age info (>5 years, etc.) → "Age: >5 years"
# # #    - Transaction type (New/Old/Renewal) → "Transaction: New"
# # #    - Validity dates → "Validity till: [date]" (e.g., "1st June 2025 to 30th June 2025", "FY 25-26")
# # #    - Decline RTO information (e.g., "Decline RTO: Dhar, Jhabua")
# # #    - Fuel type (diesel, petrol, etc.) → "Fuel Type: Diesel" (if present)
# # #    - Notes like "Decrease by 3%", "No additional deal", "irrespective of Institution", "Below 11 seater part of YTD target"
# # #    - Combine with semicolons: "Vehicle Makes: Tata; Age: >5 years; Transaction: New; Fuel Type: Diesel" (use "N/A" if nothing found)

# # # IMPORTANT: 
# # # - If a field is not found, use "N/A"
# # # - Return ONLY the JSON array, no other text
# # # - Ensure the JSON is valid and parseable
# # # - Do not extract or include the "Discount" column or its values in any field. Ignore it completely.
# # # - The "PO" column contains the Payin values - use that for the "Payin" field.
# # # - The table may have a "Discount" column - IGNORE it completely. Do not include its values anywhere, not even in remarks.
# # # IGNORE these columns completely - DO NOT extract them:
# # #    - Discount
# # #    - CD1
# # #    - Any column containing "discount" or "cd1" 
# # #    - These are not needed for our analysis

# # # Point to be Noted:
# # # - SATP means TP , so Whenever Private Car SATP is mentioned then it means PVT CAR TP
# # # - sometimes the two columns are also there in the input which are in values , like diesel or petrol, means fuel type also , so Extract that too and parse that too
# # # - Sometimes MCY means motorcycle  , so consider them in TW LOB , be it Motorcycles, scooters
# # # - Handle various formats: line-separated grids (e.g., tonnage with locations and percentages), tables with State/RTO/Fuel, emails with forwarded messages, incentives for YTD targets.
# # # - Extract month/year (e.g., "June 25", "July 25", "Aug 25", "FY 25-26") in Remarks.
# # # - For grids, create one object per row or entry (e.g., each state/RTO as a record).
# # # - If text is ambiguous, infer LOB/Segment from context (e.g., "School bus >14 seater" to "SCHOOL BUS").
# # # - Also if in the put % is mentioned in "-" , this sign is not subtraction but infact it is hyphen symbol 
# # # - Sometimes the values given in input are for example -68% , so in that case also consider it as 68% only and ignore the - sign
# # # - Sometimes segment is also mentioned as Product in the input , and remember PCI means Private Car
# # # - sometimes the two columns are also there in the input which are in values , like diesel or petrol, means fuel type also , so Extract that too and parse that too


# # # IMPORTANT DIGIT FORMAT RULES:
# # # - "Agency/PB Clusters" = Location (extract as Location)
# # # - "Agency/PB segment" = Segment (extract vehicle type, e.g., TW 1+5, PVT CAR, SC/EV, MC)
# # # - **CD2 = Payin percentage (COMPLETELY IGNORE CD1 - if CD1 columns exist, ignore them entirely)**
# # # - **Process EVERY row in the input data, including rows where 1+1 CD2 or SATP CD2 (or both) are NIL or missing**
# # # - **Create records based on CD2 values:**
# # #   - If 1+1 CD2 has a value (non-NIL), create a record with Policy="COMP", Payin=1+1 CD2
# # #   - If SATP CD2 has a value (non-NIL), create a record with Policy="TP", Payin=SATP CD2, append "SATP" to Segment
# # #   - If both 1+1 CD2 and SATP CD2 have values, create TWO records: one for COMP (using 1+1 CD2) and one for TP (using SATP CD2)
# # #   - If 1+1 CD2 is NIL but SATP CD2 has a value, create ONLY a TP record with Payin=SATP CD2, Policy="TP", append "SATP" to Segment
# # #   - If SATP CD2 is NIL but 1+1 CD2 has a value, create ONLY a COMP record with Payin=1+1 CD2, Policy="COMP"
# # #   - If both 1+1 CD2 and SATP CD2 are NIL or missing, create ONE record with Policy="COMP", Payin="0%", Remarks="Both 1+1 CD2 and SATP CD2 are NIL"

# # # SEGMENT TYPES FOR DIGIT:
# # # - **Two Wheeler (TW)**: 1+5 (New TW), 1+1 (Old PVT car and TW), 1+3 (New PVT car), SC/EV (Electric Scooter), MC (Motorcycle)
# # # - **PVT CAR**: with policy COMP + SAOD (where + means OR operator), also TP
# # # - **CV**: GVW, PCV 3 Wheeler, GCV 3W
# # # - **BUS**: School Bus, Staff Bus
# # # - **TAXI**: includes PVT Taxi
# # # - **MISD**: Tractor, Cranes, Garbage Vans

# # # POLICY TYPES:
# # # 1. **COMP** (also known as Package/First Party): for Private Car, Two Wheelers, PCV (auto, bus), GCV, MISD
# # # 2. **SAOD**: comes with Private Car and Two Wheeler
# # # 3. **Third Party (TP)**: comes with Private Car, Two Wheeler, P.C.V, G.C.V & MISD
# # # 4. **1+1 means COMP**, **SATP means TP** for formula evaluation

# # # CRITICAL CD1/CD2 HANDLING:
# # # - **IGNORE ALL CD1 VALUES COMPLETELY**
# # # - **ONLY extract values from CD2 columns**
# # # - **Create records based on CD2 values:**
# # #   - 1+1 CD2 non-NIL → Policy="COMP", Payin=1+1 CD2
# # #   - SATP CD2 non-NIL → Policy="TP", Payin=SATP CD2, Segment=Segment + " SATP"
# # #   - Both non-NIL → Create TWO records (COMP and TP)
# # #   - 1+1 CD2 NIL, SATP CD2 non-NIL → TP record only
# # #   - SATP CD2 NIL, 1+1 CD2 non-NIL → COMP record only
# # #   - Both NIL or missing → Single COMP record with Payin="0%"

# # # Extract into JSON records with these exact fields:
# # # - "Location": from Agency/PB Clusters field (use "Unknown" if missing)
# # # - "Segment": from Agency/PB segment field (include vehicle type details, append "SATP" for TP records, use "Unknown" if missing)
# # # - "Policy": "COMP" for 1+1 CD2 values, "TP" for SATP CD2 values
# # # - "Payin": from CD2 values only (format as percentage, e.g., "61.5%", use "0%" if NIL or missing)
# # # - "Remarks": ALWAYS include additional information (e.g., vehicle makes like Hero/Honda, age info like Upto 180cc, validity, etc.). If no extra info, set to "NIL". Note NIL status in remarks, e.g., "SATP CD2 is NIL", "1+1 CD2 is NIL", or "Both 1+1 CD2 and SATP CD2 are NIL"

# # # EXAMPLE OUTPUT FORMAT:
# # # output should be in the json where the key value pair should be segment,policy type,location,payin,remark,formula used 



# # # The above is for the reference purpose only , now please follow the same format and instructions to parse the input data given to you
# # # CRITICAL INSTRUCTIONS:
# # # 1. **IGNORE ALL CD1 VALUES COMPLETELY**
# # # 2. **ONLY USE CD2 VALUES FOR PAYIN**
# # # 3. **Process EVERY row in the input data, even if 1+1 CD2 or SATP CD2 (or both) are NIL or missing**
# # # 4. **Create a COMP record for non-NIL 1+1 CD2 values**
# # # 5. **Create a TP record for non-NIL SATP CD2 values, appending "SATP" to Segment**
# # # 6. **If both 1+1 CD2 and SATP CD2 have values, create TWO records**
# # # 7. **If 1+1 CD2 is NIL but SATP CD2 has a value, create TP record only**
# # # 8. **If SATP CD2 is NIL but 1+1 CD2 has a value, create COMP record only**
# # # 9. **If both 1+1 CD2 and SATP CD2 are NIL or missing, create ONE COMP record with Payin="0%"**
# # # 10. **1+1 = COMP, SATP = TP for policy determination**
# # # 11. **PVT Taxi goes under TAXI segment**
# # # 12. **MISD includes Tractor, Cranes, Garbage Vans**
# # # 13. **Parse EVERY row in the table, do not skip any row, even if one or both CD2 values are NIL**
# # # 14. **Always process all rows from the text, treating each one independently**
# # # 15. **Ensure remarks reflect NIL status clearly (e.g., "SATP CD2 is NIL", "Both 1+1 CD2 and SATP CD2 are NIL")**



# # # Return ONLY a valid JSON array, no other text.

# # # """
# # #         try:
# # #             response = client.chat.completions.create(
# # #                 model="gpt-4o-mini",
# # #                 messages=[
# # #                     {
# # #                         "role": "system", 
# # #                         "content": "You are a data extraction expert. Extract policy data as a JSON array. Convert all Payin values to percentage format. Always return valid JSON array with complete field names. Extract all additional information for remarks."
# # #                     },
# # #                     {"role": "user", "content": parse_prompt}
# # #                 ],
# # #                 temperature=0.0,
# # #                 max_tokens=4000
# # #             )
            
# # #             parsed_json = response.choices[0].message.content.strip()
# # #             logger.info(f"Raw parsing response length: {len(parsed_json)}")
            
# # #             cleaned_json = clean_json_response(parsed_json)
# # #             logger.info(f"Cleaned JSON length: {len(cleaned_json)}")
            
# # #             try:
# # #                 policy_data = json.loads(cleaned_json)
# # #                 policy_data = ensure_list_format(policy_data)
                
# # #                 if not policy_data or len(policy_data) == 0:
# # #                     raise ValueError("Parsed data is empty")
                    
# # #             except json.JSONDecodeError as e:
# # #                 logger.error(f"JSON decode error: {str(e)} with cleaned JSON: {cleaned_json[:500]}...")
# # #                 raise ValueError(f"JSON parsing failed: {str(e)}")
        
# # #         except Exception as e:
# # #             logger.error(f"Error in AI parsing: {str(e)}")
# # #             raise ValueError(f"AI parsing failed: {str(e)}")

# # #         logger.info(f"✅ Successfully parsed {len(policy_data)} policy records")

# # #         # Classify payin
# # #         logger.info("🧮 Classifying payin values...")
# # #         for record in policy_data:
# # #             try:
# # #                 if 'Discount' in record:
# # #                     del record['Discount']
# # #                 payin_val, payin_cat = classify_payin(record.get('Payin', '0%'))
# # #                 record['Payin_Value'] = payin_val
# # #                 record['Payin_Category'] = payin_cat
# # #             except Exception as e:
# # #                 logger.warning(f"Error classifying payin: {e}")
# # #                 record['Payin_Value'] = 0.0
# # #                 record['Payin_Category'] = "Payin Below 20%"

# # #         # Apply formulas
# # #         logger.info("🧮 Applying formulas and calculating payouts...")
# # #         calculated_data = apply_formula_directly(policy_data, company_name)
        
# # #         if not calculated_data or len(calculated_data) == 0:
# # #             logger.error("No data after formula application")
# # #             raise ValueError("No data after formula application")

# # #         logger.info(f"✅ Successfully calculated {len(calculated_data)} records")

# # #         # Create Excel
# # #         logger.info("📊 Creating Excel file...")
# # #         df_calc = pd.DataFrame(calculated_data)
        
# # #         if df_calc.empty:
# # #             logger.error("DataFrame is empty")
# # #             raise ValueError("DataFrame is empty")

# # #         output = BytesIO()
# # #         try:
# # #             with pd.ExcelWriter(output, engine='openpyxl') as writer:
# # #                 df_calc.to_excel(writer, sheet_name='Policy Data', startrow=2, index=False)
# # #                 worksheet = writer.sheets['Policy Data']
# # #                 headers = list(df_calc.columns)
# # #                 for col_num, value in enumerate(headers, 1):
# # #                     cell = worksheet.cell(row=3, column=col_num, value=value)
# # #                     cell.font = cell.font.copy(bold=True)
# # #                 if len(headers) > 1:
# # #                     company_cell = worksheet.cell(row=1, column=1, value=company_name)
# # #                     worksheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
# # #                     company_cell.font = company_cell.font.copy(bold=True, size=14)
# # #                     company_cell.alignment = company_cell.alignment.copy(horizontal='center')
# # #                     title_cell = worksheet.cell(row=2, column=1, value='Policy Data with Payin and Calculated Payouts')
# # #                     worksheet.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(headers))
# # #                     title_cell.font = title_cell.font.copy(bold=True, size=12)
# # #                     title_cell.alignment = title_cell.alignment.copy(horizontal='center')
# # #                 else:
# # #                     worksheet.cell(row=1, column=1, value=company_name)
# # #                     worksheet.cell(row=2, column=1, value='Policy Data with Payin and Calculated Payouts')

# # #         except Exception as e:
# # #             logger.error(f"Error creating Excel file: {str(e)}")
# # #             raise ValueError(f"Error creating Excel: {str(e)}")

# # #         output.seek(0)
# # #         excel_data = output.read()
# # #         excel_data_base64 = base64.b64encode(excel_data).decode('utf-8')

# # #         # Calculate metrics
# # #         avg_payin = sum([r.get('Payin_Value', 0) for r in calculated_data]) / len(calculated_data) if calculated_data else 0.0
# # #         unique_segments = len(set([r.get('Segment', 'N/A') for r in calculated_data]))
# # #         formula_summary = {}
# # #         for record in calculated_data:
# # #             formula = record.get('Formula Used', 'Unknown')
# # #             formula_summary[formula] = formula_summary.get(formula, 0) + 1

# # #         logger.info("✅ Processing completed successfully")
# # #         logger.info("=" * 50)
        
# # #         return {
# # #             "extracted_text": extracted_text,
# # #             "parsed_data": policy_data,
# # #             "calculated_data": calculated_data,
# # #             "excel_data": excel_data_base64,
# # #             "csv_data": df_calc.to_csv(index=False),
# # #             "json_data": json.dumps(calculated_data, indent=2),
# # #             "formula_data": FORMULA_DATA,
# # #             "metrics": {
# # #                 "total_records": len(calculated_data),
# # #                 "avg_payin": round(avg_payin, 1),
# # #                 "unique_segments": unique_segments,
# # #                 "company_name": company_name,
# # #                 "formula_summary": formula_summary
# # #             }
# # #         }

# # #     except Exception as e:
# # #         logger.error(f"Unexpected error in process_files: {str(e)}", exc_info=True)
# # #         raise

# # # @app.get("/", response_class=HTMLResponse)
# # # async def root():
# # #     """Serve a basic HTML frontend or instructions"""
# # #     try:
# # #         html_path = Path("index.html")
# # #         if html_path.exists():
# # #             with open(html_path, "r", encoding="utf-8") as f:
# # #                 html_content = f.read()
# # #             return HTMLResponse(content=html_content)
# # #         else:
# # #             html_content = """
# # #             <h1>Insurance Policy Processing System</h1>
# # #             <p>Welcome to the Insurance Policy Processing API.</p>
# # #             <h2>Usage Instructions:</h2>
# # #             <ul>
# # #                 <li><b>Endpoint:</b> POST /process</li>
# # #                 <li><b>Parameters:</b>
# # #                     <ul>
# # #                         <li><b>company_name</b>: String (form-data, required)</li>
# # #                         <li><b>policy_file</b>: Image file (PNG, JPG, JPEG, GIF, BMP, TIFF; file upload, required)</li>
# # #                     </ul>
# # #                 </li>
# # #                 <li><b>Response:</b> JSON object containing extracted text, parsed data, calculated data, Excel/CSV/JSON files, and metrics.</li>
# # #                 <li><b>Health Check:</b> GET /health</li>
# # #             </ul>
# # #             <h2>Features:</h2>
# # #             <ul>
# # #                 <li>AI-powered OCR using GPT-4o for text extraction</li>
# # #                 <li>Structured data parsing with detailed remarks</li>
# # #                 <li>Payout calculations based on embedded formula rules</li>
# # #                 <li>Downloadable Excel, CSV, and JSON outputs</li>
# # #             </ul>
# # #             """
# # #             return HTMLResponse(content=html_content)
# # #     except Exception as e:
# # #         logger.error(f"Error serving HTML: {str(e)}")
# # #         return HTMLResponse(content=f"<h1>Error loading page</h1><p>{str(e)}</p>", status_code=500)

# # # @app.post("/process")
# # # async def process_policy(company_name: str = Form(...), policy_file: UploadFile = File(...)):
# # #     """Process policy image and return extracted and calculated data"""
# # #     try:
# # #         logger.info("=" * 50)
# # #         logger.info(f"📨 Received request for company: {company_name}")
# # #         logger.info(f"📄 File: {policy_file.filename}, Content-Type: {policy_file.content_type}")
        
# # #         # Read file
# # #         policy_file_bytes = await policy_file.read()
# # #         if len(policy_file_bytes) == 0:
# # #             logger.error("Uploaded file is empty")
# # #             return JSONResponse(
# # #                 status_code=400,
# # #                 content={"error": "Uploaded file is empty"}
# # #             )

# # #         logger.info(f"📦 File size: {len(policy_file_bytes)} bytes")
        
# # #         # Process
# # #         results = process_files(
# # #             policy_file_bytes, 
# # #             policy_file.filename, 
# # #             policy_file.content_type,
# # #             company_name
# # #         )
        
# # #         logger.info("✅ Returning results to client")
# # #         return JSONResponse(content=results)
        
# # #     except ValueError as e:
# # #         logger.error(f"Validation error: {str(e)}")
# # #         return JSONResponse(
# # #             status_code=400,
# # #             content={"error": str(e)}
# # #         )
# # #     except Exception as e:
# # #         logger.error(f"Error processing request: {str(e)}", exc_info=True)
# # #         return JSONResponse(
# # #             status_code=500,
# # #             content={"error": f"Processing failed: {str(e)}"}
# # #         )

# # # @app.get("/health")
# # # async def health_check():
# # #     """Health check endpoint"""
# # #     return JSONResponse(content={"status": "healthy", "message": "Server is running"})

# # # if __name__ == "__main__":
# # #     import uvicorn
# # #     logger.info("🚀 Starting Insurance Policy Processing System...")
# # #     logger.info("📡 Server will be available at: http://localhost:8000")
# # #     logger.info("🔑 OpenAI API Key is configured: ✅")
# # #     uvicorn.run(app, host="0.0.0.0", port=8000)

# # from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# # from fastapi.responses import JSONResponse, HTMLResponse
# # from fastapi.middleware.cors import CORSMiddleware
# # from io import BytesIO
# # import base64
# # import json
# # import os
# # from dotenv import load_dotenv
# # import logging
# # import re
# # import pandas as pd
# # from openai import OpenAI
# # from pathlib import Path

# # # Configure logging
# # logging.basicConfig(
# #     level=logging.INFO,
# #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# # )
# # logger = logging.getLogger(__name__)

# # # Load environment variables
# # load_dotenv()

# # # Load OpenAI API key
# # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# # if not OPENAI_API_KEY:
# #     logger.error("⚠️ OPENAI_API_KEY environment variable not set")
# #     raise RuntimeError("OPENAI_API_KEY environment variable not set. Please create a .env file with OPENAI_API_KEY=your-key")

# # # Initialize OpenAI client
# # try:
# #     client = OpenAI(api_key=OPENAI_API_KEY)
# #     logger.info("✅ OpenAI client initialized successfully")
# # except Exception as e:
# #     logger.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
# #     raise RuntimeError(f"Failed to initialize OpenAI client: {str(e)}")

# # app = FastAPI(title="Insurance Policy Processing System")

# # # Add CORS middleware for frontend compatibility
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],  # <-- allow all origins in development (use specific origins in production)
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Embedded Formula Data
# # FORMULA_DATA = [
# #     {"LOB": "TW", "SEGMENT": "1+5", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "NIL"},
# #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "NIL"},
# #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
# #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
# #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-5%", "REMARKS": "Payin Above 50%"},
# #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Bajaj, Digit, ICICI", "PO": "-3%", "REMARKS": "Payin Above 20%"},
# #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
# #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
# #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
# #     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR COMP + SAOD", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "All Fuel"},
# #     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Bajaj, Digit, SBI", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# #     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Bajaj, Digit, SBI", "PO": "-3%", "REMARKS": "Payin Above 20%"},
# #     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Rest of Companies", "PO": "90% of Payin", "REMARKS": "Zuno - 21"},
# #     {"LOB": "CV", "SEGMENT": "Upto 2.5 GVW", "INSURER": "Reliance, SBI", "PO": "-2%", "REMARKS": "NIL"},
# #     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# #     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
# #     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
# #     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
# #     {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "INSURER": "TATA, Reliance, Digit, ICICI", "PO": "Less 2% of Payin", "REMARKS": "NIL"},
# #     {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "INSURER": "Rest of Companies", "PO": "88% of Payin", "REMARKS": "NIL"},
# #     {"LOB": "BUS", "SEGMENT": "STAFF BUS", "INSURER": "All Companies", "PO": "88% of Payin", "REMARKS": "NIL"},
# #     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# #     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
# #     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
# #     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
# #     {"LOB": "MISD", "SEGMENT": "Misd, Tractor", "INSURER": "All Companies", "PO": "88% of Payin", "REMARKS": "NIL"}
# # ]

# # def extract_text_from_file(file_bytes: bytes, filename: str, content_type: str) -> str:
# #     """Extract text from uploaded image file and structure it into JSON with specified keys"""
# #     file_extension = filename.split('.')[-1].lower() if '.' in filename else ''
# #     file_type = content_type if content_type else file_extension

# #     # Image-based extraction with structured JSON output
# #     image_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
# #     if file_extension in image_extensions or file_type.startswith('image/'):
# #         try:
# #             image_base64 = base64.b64encode(file_bytes).decode('utf-8')
            
# #             prompt = """
# #             Extract the text from the image. Please segregate everything based on the segment, policy type, location, payin, and remark as the keys.
# #             Please give me in the JSON format.
# #             - payin is in percentage, values in the range of 0 to 100.
# #             - Put the rest of the information into the remarks.
# #             - Points to remember:
# #               - Ignore CD1, CD2 is the payin or payrate.
# #               - cluster is the location.
# #               - Data can be in table format.
# #               - Policy types are SATP (which is TP) and Comp.
# #               - Ignore CD1.
# #               - Comp and TP columns can have sub-columns like CD1 and CD2, so focus on CD2.
# #               - 1+1 means Comp, in TW new, it means TW LOB and 1+5 Segment.
# #               - Agency, PB clusters are the locations.
# #               - If policy type is not mentioned, consider Comp/TP.
# #             - Please identify the Segments when parsing.
# #               - For example, if the information is regarding a private car and policy type is TP or third party, then Segment should be PVT CAR TP.
# #             - For the provided image, if PCV3w is mentioned, it falls under CV LOB and the segment should be "All GVW & PCV 3W, GCV 3W".
# #             - Handle negative percentages (e.g., -68%) by treating them as positive (68%).
# #             - Include additional details like minimum premium conditions in remarks.
# #             Return ONLY valid JSON array, no markdown formatting.
# #             """

# #             response = client.chat.completions.create(
# #                 model="gpt-4o",
# #                 messages=[{
# #                     "role": "user",
# #                     "content": [
# #                         {"type": "text", "text": prompt},
# #                         {"type": "image_url", "image_url": {"url": f"data:image/{file_extension};base64,{image_base64}"}}
# #                     ]
# #                 }],
# #                 temperature=0.0,
# #                 max_tokens=4000
# #             )
            
# #             extracted_text = response.choices[0].message.content.strip()
            
# #             if not extracted_text or len(extracted_text) < 10:
# #                 logger.error("OCR returned very short or empty text")
# #                 return "[]"
            
# #             return extracted_text
            
# #         except Exception as e:
# #             logger.error(f"Error in OCR extraction: {str(e)}")
# #             return "[]"

# #     raise ValueError(f"Unsupported file type for {filename}. Only images are supported.")

# # def clean_json_response(response_text: str) -> str:
# #     """Clean and extract valid JSON array from OpenAI response"""
# #     cleaned = re.sub(r'```json\s*|\s*```', '', response_text).strip()
    
# #     start_idx = cleaned.find('[')
# #     end_idx = cleaned.rfind(']') + 1 if cleaned.rfind(']') != -1 else len(cleaned)
    
# #     if start_idx != -1 and end_idx > start_idx:
# #         cleaned = cleaned[start_idx:end_idx]
# #     else:
# #         logger.warning("No valid JSON array found in response, returning empty array")
# #         return "[]"
    
# #     if not cleaned.startswith('['):
# #         cleaned = '[' + cleaned
# #     if not cleaned.endswith(']'):
# #         cleaned += ']'
    
# #     return cleaned

# # def ensure_list_format(data) -> list:
# #     """Ensure data is in list format"""
# #     if isinstance(data, list):
# #         return data
# #     elif isinstance(data, dict):
# #         return [data]
# #     else:
# #         raise ValueError(f"Expected list or dict, got {type(data)}")

# # def classify_payin(payin_str):
# #     """Converts Payin string to float and classifies its range"""
# #     try:
# #         payin_clean = str(payin_str).replace('%', '').replace(' ', '').strip()
        
# #         if not payin_clean or payin_clean.upper() == 'N/A':
# #             return 0.0, "Payin Below 20%"
        
# #         # Handle negative signs as hyphens (convert to positive)
# #         payin_clean = payin_clean.replace('-', '')
# #         payin_value = float(payin_clean)
        
# #         if payin_value <= 20:
# #             category = "Payin Below 20%"
# #         elif 21 <= payin_value <= 30:
# #             category = "Payin 21% to 30%"
# #         elif 31 <= payin_value <= 50:
# #             category = "Payin 31% to 50%"
# #         else:
# #             category = "Payin Above 50%"
# #         return payin_value, category
# #     except (ValueError, TypeError) as e:
# #         logger.warning(f"Could not parse payin value: {payin_str}, error: {e}")
# #         return 0.0, "Payin Below 20%"

# # def apply_formula_directly(policy_data, company_name):
# #     """Apply formula rules directly using Python logic with default STAFF BUS for unspecified BUS"""
# #     if not policy_data:
# #         logger.warning("No policy data to process")
# #         return []
    
# #     calculated_data = []
    
# #     for record in policy_data:
# #         try:
# #             segment = str(record.get('segment', '')).upper()
# #             payin_value = record.get('payin', 0)
# #             payin_category = record.get('Payin_Category', '')
            
# #             lob = ""
# #             segment_upper = segment.upper()
            
# #             if any(tw_keyword in segment_upper for tw_keyword in ['TW', '2W', 'TWO WHEELER', 'TWO-WHEELER', 'MCY', 'MC', 'SC']):
# #                 lob = "TW"
# #             elif any(car_keyword in segment_upper for car_keyword in ['PVT CAR', 'PRIVATE CAR', 'CAR', 'PCI']):
# #                 lob = "PVT CAR"
# #             elif any(cv_keyword in segment_upper for cv_keyword in ['CV', 'COMMERCIAL', 'LCV', 'GVW', 'TN', 'UPTO', 'ALL GVW', 'PCV', 'GCV']):
# #                 lob = "CV"
# #             elif 'BUS' in segment_upper:
# #                 lob = "BUS"
# #             elif 'TAXI' in segment_upper:
# #                 lob = "TAXI"
# #             elif any(misd_keyword in segment_upper for misd_keyword in ['MISD', 'TRACTOR', 'MISC', 'AMBULANCE', 'POLICE VAN', 'GARBAGE VAN']):
# #                 lob = "MISD"
# #             else:
# #                 remarks_upper = str(record.get('remark', '')).upper()
# #                 if any(cv_keyword in remarks_upper for cv_keyword in ['TATA', 'MARUTI', 'GVW', 'TN']):
# #                     lob = "CV"
# #                 else:
# #                     lob = "UNKNOWN" 
            
# #             matched_segment = segment_upper
# #             if lob == "BUS":
# #                 if "SCHOOL" not in segment_upper and "STAFF" not in segment_upper:
# #                     matched_segment = "STAFF BUS"
# #                 elif "SCHOOL" in segment_upper:
# #                     matched_segment = "SCHOOL BUS"
# #                 elif "STAFF" in segment_upper:
# #                     matched_segment = "STAFF BUS"
            
# #             matched_rule = None
# #             rule_explanation = ""
# #             company_normalized = company_name.upper().replace('GENERAL', '').replace('INSURANCE', '').strip()
            
# #             for rule in FORMULA_DATA:
# #                 if rule["LOB"] != lob:
# #                     continue
                    
# #                 rule_segment = rule["SEGMENT"].upper()
# #                 segment_match = False
                
# #                 if lob == "CV":
# #                     if "UPTO 2.5" in rule_segment:
# #                         if any(keyword in segment_upper for keyword in ["UPTO 2.5", "2.5 TN", "2.5 GVW", "2.5TN", "2.5GVW", "UPTO2.5"]):
# #                             segment_match = True
# #                     elif "ALL GVW" in rule_segment:
# #                         segment_match = True
# #                 elif lob == "BUS":
# #                     if matched_segment == rule_segment:
# #                         segment_match = True
# #                 elif lob == "PVT CAR":
# #                     if "COMP" in rule_segment and any(keyword in segment for keyword in ["COMP", "COMPREHENSIVE", "PACKAGE", "1ST PARTY", "1+1"]):
# #                         segment_match = True
# #                     elif "TP" in rule_segment and "TP" in segment and "COMP" not in segment:
# #                         segment_match = True
# #                 elif lob == "TW":
# #                     if "1+5" in rule_segment and any(keyword in segment for keyword in ["1+5", "NEW", "FRESH"]):
# #                         segment_match = True
# #                     elif "SAOD + COMP" in rule_segment and any(keyword in segment for keyword in ["SAOD", "COMP", "PACKAGE", "1ST PARTY", "1+1"]):
# #                         segment_match = True
# #                     elif "TP" in rule_segment and "TP" in segment:
# #                         segment_match = True
# #                 else:
# #                     segment_match = True
                
# #                 if not segment_match:
# #                     continue
                
# #                 insurers = [ins.strip().upper() for ins in rule["INSURER"].split(',')]
# #                 company_match = False
                
# #                 if "ALL COMPANIES" in insurers:
# #                     company_match = True
# #                 elif "REST OF COMPANIES" in insurers:
# #                     is_in_specific_list = False
# #                     for other_rule in FORMULA_DATA:
# #                         if (other_rule["LOB"] == rule["LOB"] and 
# #                             other_rule["SEGMENT"] == rule["SEGMENT"] and
# #                             "REST OF COMPANIES" not in other_rule["INSURER"] and
# #                             "ALL COMPANIES" not in other_rule["INSURER"]):
# #                             other_insurers = [ins.strip().upper() for ins in other_rule["INSURER"].split(',')]
# #                             if any(company_key in company_normalized for company_key in other_insurers):
# #                                 is_in_specific_list = True
# #                                 break
# #                     if not is_in_specific_list:
# #                         company_match = True
# #                 else:
# #                     for insurer in insurers:
# #                         if insurer in company_normalized or company_normalized in insurer:
# #                             company_match = True
# #                             break
                
# #                 if not company_match:
# #                     continue
                
# #                 remarks = rule.get("REMARKS", "")
                
# #                 if remarks == "NIL" or "NIL" in remarks.upper():
# #                     matched_rule = rule
# #                     rule_explanation = f"Direct match: LOB={lob}, Segment={rule_segment}, Company={rule['INSURER']}"
# #                     break
# #                 elif any(payin_keyword in remarks for payin_keyword in ["Payin Below", "Payin 21%", "Payin 31%", "Payin Above"]):
# #                     if payin_category in remarks:
# #                         matched_rule = rule
# #                         rule_explanation = f"Payin category match: LOB={lob}, Segment={rule_segment}, Payin={payin_category}"
# #                         break
# #                 else:
# #                     matched_rule = rule
# #                     rule_explanation = f"Other remarks match: LOB={lob}, Segment={rule_segment}, Remarks={remarks}"
# #                     break
            
# #             if matched_rule:
# #                 po_formula = matched_rule["PO"]
# #                 calculated_payout = payin_value
                
# #                 if "90% of Payin" in po_formula:
# #                     calculated_payout *= 0.9
# #                 elif "88% of Payin" in po_formula:
# #                     calculated_payout *= 0.88
# #                 elif "Less 2% of Payin" in po_formula:
# #                     calculated_payout -= 2
# #                 elif "-2%" in po_formula:
# #                     calculated_payout -= 2
# #                 elif "-3%" in po_formula:
# #                     calculated_payout -= 3
# #                 elif "-4%" in po_formula:
# #                     calculated_payout -= 4
# #                 elif "-5%" in po_formula:
# #                     calculated_payout -= 5
                
# #                 calculated_payout = max(0, calculated_payout)
# #                 formula_used = po_formula
# #             else:
# #                 calculated_payout = payin_value
# #                 formula_used = "No matching rule found"
            
# #             result_record = {
# #                 'segment': segment,
# #                 'policy type': record.get('policy type', 'Comp/TP'),
# #                 'location': record.get('location', 'N/A'),
# #                 'payin': f"{payin_value}%",
# #                 'remark': record.get('remark', []),
# #                 'Calculated Payout': f"{calculated_payout:.2f}%",
# #                 'Formula Used': formula_used,
# #                 'Rule Explanation': rule_explanation
# #             }
            
# #             calculated_data.append(result_record)
            
# #         except Exception as e:
# #             logger.error(f"Error processing record: {record}, error: {str(e)}")
# #             result_record = {
# #                 'segment': segment,
# #                 'policy type': record.get('policy type', 'Comp/TP'),
# #                 'location': record.get('location', 'N/A'),
# #                 'payin': f"{payin_value}%",
# #                 'remark': record.get('remark', ['Error']),
# #                 'Calculated Payout': "Error",
# #                 'Formula Used': "Error in calculation",
# #                 'Rule Explanation': f"Error: {str(e)}"
# #             }
# #             calculated_data.append(result_record)
    
# #     return calculated_data

# # def process_files(policy_file_bytes: bytes, policy_filename: str, policy_content_type: str, company_name: str):
# #     """Main processing function with enhanced error handling"""
# #     try:
# #         logger.info("=" * 50)
# #         logger.info(f"🚀 Starting file processing for {policy_filename}...")
# #         logger.info(f"📁 File size: {len(policy_file_bytes)} bytes")
        
# #         # Extract text
# #         logger.info("🔍 Extracting text from policy image...")
# #         extracted_text = extract_text_from_file(policy_file_bytes, policy_filename, policy_content_type)
# #         logger.info(f"✅ Extracted text length: {len(extracted_text)} chars")

# #         if not extracted_text.strip():
# #             logger.error("No text extracted from the image")
# #             raise ValueError("No text could be extracted. Please ensure the image is clear and contains readable text.")

# #         # Parse with AI
# #         logger.info("🧠 Parsing policy data with AI...")
        
# #         try:
# #             policy_data = json.loads(extracted_text)
# #             policy_data = ensure_list_format(policy_data)
            
# #             if not policy_data or len(policy_data) == 0:
# #                 raise ValueError("Parsed data is empty")
                    
# #         except json.JSONDecodeError as e:
# #             logger.error(f"JSON decode error: {str(e)} with cleaned JSON: {extracted_text[:500]}...")
# #             raise ValueError(f"JSON parsing failed: {str(e)}")
        
# #         logger.info(f"✅ Successfully parsed {len(policy_data)} policy records")

# #         # Classify payin
# #         logger.info("🧮 Classifying payin values...")
# #         for record in policy_data:
# #             try:
# #                 payin_val, payin_cat = classify_payin(record.get('payin', '0%'))
# #                 record['Payin_Value'] = payin_val
# #                 record['Payin_Category'] = payin_cat
# #             except Exception as e:
# #                 logger.warning(f"Error classifying payin: {e}")
# #                 record['Payin_Value'] = 0.0
# #                 record['Payin_Category'] = "Payin Below 20%"

# #         # Apply formulas
# #         logger.info("🧮 Applying formulas and calculating payouts...")
# #         calculated_data = apply_formula_directly(policy_data, company_name)
        
# #         if not calculated_data or len(calculated_data) == 0:
# #             logger.error("No data after formula application")
# #             raise ValueError("No data after formula application")

# #         logger.info(f"✅ Successfully calculated {len(calculated_data)} records")

# #         # Create Excel
# #         logger.info("📊 Creating Excel file...")
# #         df_calc = pd.DataFrame(calculated_data)
        
# #         if df_calc.empty:
# #             logger.error("DataFrame is empty")
# #             raise ValueError("DataFrame is empty")

# #         output = BytesIO()
# #         try:
# #             with pd.ExcelWriter(output, engine='openpyxl') as writer:
# #                 df_calc.to_excel(writer, sheet_name='Policy Data', startrow=2, index=False)
# #                 worksheet = writer.sheets['Policy Data']
# #                 headers = list(df_calc.columns)
# #                 for col_num, value in enumerate(headers, 1):
# #                     cell = worksheet.cell(row=3, column=col_num, value=value)
# #                     cell.font = cell.font.copy(bold=True)
# #                 if len(headers) > 1:
# #                     company_cell = worksheet.cell(row=1, column=1, value=company_name)
# #                     worksheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
# #                     company_cell.font = company_cell.font.copy(bold=True, size=14)
# #                     company_cell.alignment = company_cell.alignment.copy(horizontal='center')
# #                     title_cell = worksheet.cell(row=2, column=1, value='Policy Data with Payin and Calculated Payouts')
# #                     worksheet.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(headers))
# #                     title_cell.font = title_cell.font.copy(bold=True, size=12)
# #                     title_cell.alignment = title_cell.alignment.copy(horizontal='center')
# #                 else:
# #                     worksheet.cell(row=1, column=1, value=company_name)
# #                     worksheet.cell(row=2, column=1, value='Policy Data with Payin and Calculated Payouts')

# #         except Exception as e:
# #             logger.error(f"Error creating Excel file: {str(e)}")
# #             raise ValueError(f"Error creating Excel: {str(e)}")

# #         output.seek(0)
# #         excel_data = output.read()
# #         excel_data_base64 = base64.b64encode(excel_data).decode('utf-8')

# #         # Calculate metrics
# #         avg_payin = sum([r.get('Payin_Value', 0) for r in calculated_data]) / len(calculated_data) if calculated_data else 0.0
# #         unique_segments = len(set([r.get('segment', 'N/A') for r in calculated_data]))
# #         formula_summary = {}
# #         for record in calculated_data:
# #             formula = record.get('Formula Used', 'Unknown')
# #             formula_summary[formula] = formula_summary.get(formula, 0) + 1

# #         logger.info("✅ Processing completed successfully")
# #         logger.info("=" * 50)
        
# #         return {
# #             "extracted_text": extracted_text,
# #             "parsed_data": policy_data,
# #             "calculated_data": calculated_data,
# #             "excel_data": excel_data_base64,
# #             "csv_data": df_calc.to_csv(index=False),
# #             "json_data": json.dumps(calculated_data, indent=2),
# #             "formula_data": FORMULA_DATA,
# #             "metrics": {
# #                 "total_records": len(calculated_data),
# #                 "avg_payin": round(avg_payin, 1),
# #                 "unique_segments": unique_segments,
# #                 "company_name": company_name,
# #                 "formula_summary": formula_summary
# #             }
# #         }

# #     except Exception as e:
# #         logger.error(f"Unexpected error in process_files: {str(e)}", exc_info=True)
# #         raise

# # @app.get("/", response_class=HTMLResponse)
# # async def root():
# #     """Serve a basic HTML frontend or instructions"""
# #     try:
# #         html_path = Path("index.html")
# #         if html_path.exists():
# #             with open(html_path, "r", encoding="utf-8") as f:
# #                 html_content = f.read()
# #             return HTMLResponse(content=html_content)
# #         else:
# #             html_content = """
# #             <h1>Insurance Policy Processing System</h1>
# #             <p>Welcome to the Insurance Policy Processing API.</p>
# #             <h2>Usage Instructions:</h2>
# #             <ul>
# #                 <li><b>Endpoint:</b> POST /process</li>
# #                 <li><b>Parameters:</b>
# #                     <ul>
# #                         <li><b>company_name</b>: String (form-data, required)</li>
# #                         <li><b>policy_file</b>: Image file (PNG, JPG, JPEG, GIF, BMP, TIFF; file upload, required)</li>
# #                     </ul>
# #                 </li>
# #                 <li><b>Response:</b> JSON object containing extracted text, parsed data, calculated data, Excel/CSV/JSON files, and metrics.</li>
# #                 <li><b>Health Check:</b> GET /health</li>
# #             </ul>
# #             <h2>Features:</h2>
# #             <ul>
# #                 <li>AI-powered OCR using GPT-4o for text extraction</li>
# #                 <li>Structured data parsing with detailed remarks</li>
# #                 <li>Payout calculations based on embedded formula rules</li>
# #                 <li>Downloadable Excel, CSV, and JSON outputs</li>
# #             </ul>
# #             """
# #             return HTMLResponse(content=html_content)
# #     except Exception as e:
# #         logger.error(f"Error serving HTML: {str(e)}")
# #         return HTMLResponse(content=f"<h1>Error loading page</h1><p>{str(e)}</p>", status_code=500)

# # @app.post("/process")
# # async def process_policy(company_name: str = Form(...), policy_file: UploadFile = File(...)):
# #     """Process policy image and return extracted and calculated data"""
# #     try:
# #         logger.info("=" * 50)
# #         logger.info(f"📨 Received request for company: {company_name}")
# #         logger.info(f"📄 File: {policy_file.filename}, Content-Type: {policy_file.content_type}")
        
# #         # Read file
# #         policy_file_bytes = await policy_file.read()
# #         if len(policy_file_bytes) == 0:
# #             logger.error("Uploaded file is empty")
# #             return JSONResponse(
# #                 status_code=400,
# #                 content={"error": "Uploaded file is empty"}
# #             )

# #         logger.info(f"📦 File size: {len(policy_file_bytes)} bytes")
        
# #         # Process
# #         results = process_files(
# #             policy_file_bytes, 
# #             policy_file.filename, 
# #             policy_file.content_type,
# #             company_name
# #         )
        
# #         logger.info("✅ Returning results to client")
# #         return JSONResponse(content=results)
        
# #     except ValueError as e:
# #         logger.error(f"Validation error: {str(e)}")
# #         return JSONResponse(
# #             status_code=400,
# #             content={"error": str(e)}
# #         )
# #     except Exception as e:
# #         logger.error(f"Error processing request: {str(e)}", exc_info=True)
# #         return JSONResponse(
# #             status_code=500,
# #             content={"error": f"Processing failed: {str(e)}"}
# #         )

# # @app.get("/health")
# # async def health_check():
# #     """Health check endpoint"""
# #     return JSONResponse(content={"status": "healthy", "message": "Server is running"})

# # if __name__ == "__main__":
# #     import uvicorn
# #     logger.info("🚀 Starting Insurance Policy Processing System...")
# #     logger.info("📡 Server will be available at: http://localhost:8000")
# #     logger.info("🔑 OpenAI API Key is configured: ✅")
# #     uvicorn.run(app, host="0.0.0.0", port=8000)



# # from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# # from fastapi.responses import JSONResponse, HTMLResponse
# # from fastapi.middleware.cors import CORSMiddleware
# # from io import BytesIO
# # import base64
# # import json
# # import os
# # from dotenv import load_dotenv
# # import logging
# # import re
# # import pandas as pd
# # from openai import OpenAI
# # from pathlib import Path

# # # Configure logging
# # logging.basicConfig(
# #     level=logging.INFO,
# #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# # )
# # logger = logging.getLogger(__name__)

# # # Load environment variables
# # load_dotenv()

# # # Load OpenAI API key
# # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# # if not OPENAI_API_KEY:
# #     logger.error("⚠️ OPENAI_API_KEY environment variable not set")
# #     raise RuntimeError("OPENAI_API_KEY environment variable not set. Please create a .env file with OPENAI_API_KEY=your-key")

# # # Initialize OpenAI client
# # try:
# #     client = OpenAI(api_key=OPENAI_API_KEY)
# #     logger.info("✅ OpenAI client initialized successfully")
# # except Exception as e:
# #     logger.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
# #     raise RuntimeError(f"Failed to initialize OpenAI client: {str(e)}")

# # app = FastAPI(title="Insurance Policy Processing System")

# # # Add CORS middleware for frontend compatibility
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],  # <-- allow all origins in development (use specific origins in production)
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Embedded Formula Data
# # FORMULA_DATA = [
# #     {"LOB": "TW", "SEGMENT": "1+5", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "NIL"},
# #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "NIL"},
# #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
# #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
# #     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-5%", "REMARKS": "Payin Above 50%"},
# #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Bajaj, Digit, ICICI", "PO": "-3%", "REMARKS": "Payin Above 20%"},
# #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
# #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
# #     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
# #     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR COMP + SAOD", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "All Fuel"},
# #     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Bajaj, Digit, SBI", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# #     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Bajaj, Digit, SBI", "PO": "-3%", "REMARKS": "Payin Above 20%"},
# #     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Rest of Companies", "PO": "90% of Payin", "REMARKS": "Zuno - 21"},
# #     {"LOB": "CV", "SEGMENT": "Upto 2.5 GVW", "INSURER": "Reliance, SBI", "PO": "-2%", "REMARKS": "NIL"},
# #     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# #     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
# #     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
# #     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
# #     {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "INSURER": "TATA, Reliance, Digit, ICICI", "PO": "Less 2% of Payin", "REMARKS": "NIL"},
# #     {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "INSURER": "Rest of Companies", "PO": "88% of Payin", "REMARKS": "NIL"},
# #     {"LOB": "BUS", "SEGMENT": "STAFF BUS", "INSURER": "All Companies", "PO": "88% of Payin", "REMARKS": "NIL"},
# #     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
# #     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
# #     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
# #     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
# #     {"LOB": "MISD", "SEGMENT": "Misd, Tractor", "INSURER": "All Companies", "PO": "88% of Payin", "REMARKS": "NIL"}
# # ]

# # def extract_text_from_file(file_bytes: bytes, filename: str, content_type: str) -> str:
# #     """Extract text from uploaded image file and structure it into JSON with specified keys"""
# #     file_extension = filename.split('.')[-1].lower() if '.' in filename else ''
# #     file_type = content_type if content_type else file_extension

# #     # Image-based extraction with structured JSON output
# #     image_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
# #     if file_extension in image_extensions or file_type.startswith('image/'):
# #         try:
# #             image_base64 = base64.b64encode(file_bytes).decode('utf-8')
            
# #             prompt = """
# #             Extract the text from the image. Please segregate everything based on the segment, policy type, location, payin, and remark as the keys.
# #             Please give me in the JSON format.
# #             - payin is in percentage, values in the range of 0 to 100.
# #             - Put the rest of the information into the remarks.
# #             - Points to remember:
# #               - Ignore CD1, CD2 is the payin or payrate.
# #               - cluster is the location.
# #               - Data can be in table format.
# #               - Policy types are SATP (which is TP) and Comp.
# #               - Ignore CD1.
# #               - Comp and TP columns can have sub-columns like CD1 and CD2, so focus on CD2.
# #               - 1+1 means Comp, in TW new, it means TW LOB and 1+5 Segment.
# #               - Agency, PB clusters are the locations.
# #               - If policy type is not mentioned, consider Comp/TP.
# #             - Please identify the Segments when parsing.
# #               - For example, if the information is regarding a private car and policy type is TP or third party, then Segment should be PVT CAR TP.
# #             - For the provided image, if PCV3w is mentioned, it falls under CV LOB and the segment should be "All GVW & PCV 3W, GCV 3W".
# #             - Handle negative percentages (e.g., -68%) by treating them as positive (68%).
# #             - Include additional details like minimum premium conditions in remarks.
# #             Return ONLY valid JSON array, no markdown formatting.
# #             """

# #             response = client.chat.completions.create(
# #                 model="gpt-4o",
# #                 messages=[{
# #                     "role": "user",
# #                     "content": [
# #                         {"type": "text", "text": prompt},
# #                         {"type": "image_url", "image_url": {"url": f"data:image/{file_extension};base64,{image_base64}"}}
# #                     ]
# #                 }],
# #                 temperature=0.0,
# #                 max_tokens=4000
# #             )
            
# #             extracted_text = response.choices[0].message.content.strip()
            
# #             # Remove Markdown formatting
# #             cleaned_text = re.sub(r'```json
# #             if not cleaned_text:
# #                 logger.error("Cleaned text is empty after removing Markdown")
# #                 return "[]"
            
# #             return cleaned_text
            
# #         except Exception as e:
# #             logger.error(f"Error in OCR extraction: {str(e)}")
# #             return "[]"

# #     raise ValueError(f"Unsupported file type for {filename}. Only images are supported.")

# # def clean_json_response(response_text: str) -> str:
# #     """Clean and extract valid JSON array from OpenAI response"""
# #     cleaned = re.sub(r'```json\s*|\s*```', '', response_text).strip()
    
# #     start_idx = cleaned.find('[')
# #     end_idx = cleaned.rfind(']') + 1 if cleaned.rfind(']') != -1 else len(cleaned)
    
# #     if start_idx != -1 and end_idx > start_idx:
# #         cleaned = cleaned[start_idx:end_idx]
# #     else:
# #         logger.warning("No valid JSON array found in response, returning empty array")
# #         return "[]"
    
# #     if not cleaned.startswith('['):
# #         cleaned = '[' + cleaned
# #     if not cleaned.endswith(']'):
# #         cleaned += ']'
    
# #     return cleaned

# # def ensure_list_format(data) -> list:
# #     """Ensure data is in list format"""
# #     if isinstance(data, list):
# #         return data
# #     elif isinstance(data, dict):
# #         return [data]
# #     else:
# #         raise ValueError(f"Expected list or dict, got {type(data)}")

# # def classify_payin(payin_str):
# #     """Converts Payin string to float and classifies its range"""
# #     try:
# #         payin_clean = str(payin_str).replace('%', '').replace(' ', '').strip()
        
# #         if not payin_clean or payin_clean.upper() == 'N/A':
# #             return 0.0, "Payin Below 20%"
        
# #         # Handle negative signs as hyphens (convert to positive)
# #         payin_clean = payin_clean.replace('-', '')
# #         payin_value = float(payin_clean)
        
# #         if payin_value <= 20:
# #             category = "Payin Below 20%"
# #         elif 21 <= payin_value <= 30:
# #             category = "Payin 21% to 30%"
# #         elif 31 <= payin_value <= 50:
# #             category = "Payin 31% to 50%"
# #         else:
# #             category = "Payin Above 50%"
# #         return payin_value, category
# #     except (ValueError, TypeError) as e:
# #         logger.warning(f"Could not parse payin value: {payin_str}, error: {e}")
# #         return 0.0, "Payin Below 20%"

# # def apply_formula_directly(policy_data, company_name):
# #     """Apply formula rules directly using Python logic with default STAFF BUS for unspecified BUS"""
# #     if not policy_data:
# #         logger.warning("No policy data to process")
# #         return []
    
# #     calculated_data = []
    
# #     for record in policy_data:
# #         try:
# #             segment = str(record.get('segment', '')).upper()
# #             payin_value = record.get('payin', 0)
# #             payin_category = record.get('Payin_Category', '')
            
# #             lob = ""
# #             segment_upper = segment.upper()
            
# #             if any(tw_keyword in segment_upper for tw_keyword in ['TW', '2W', 'TWO WHEELER', 'TWO-WHEELER', 'MCY', 'MC', 'SC']):
# #                 lob = "TW"
# #             elif any(car_keyword in segment_upper for car_keyword in ['PVT CAR', 'PRIVATE CAR', 'CAR', 'PCI']):
# #                 lob = "PVT CAR"
# #             elif any(cv_keyword in segment_upper for cv_keyword in ['CV', 'COMMERCIAL', 'LCV', 'GVW', 'TN', 'UPTO', 'ALL GVW', 'PCV', 'GCV']):
# #                 lob = "CV"
# #             elif 'BUS' in segment_upper:
# #                 lob = "BUS"
# #             elif 'TAXI' in segment_upper:
# #                 lob = "TAXI"
# #             elif any(misd_keyword in segment_upper for misd_keyword in ['MISD', 'TRACTOR', 'MISC', 'AMBULANCE', 'POLICE VAN', 'GARBAGE VAN']):
# #                 lob = "MISD"
# #             else:
# #                 remarks_upper = str(record.get('remark', '')).upper()
# #                 if any(cv_keyword in remarks_upper for cv_keyword in ['TATA', 'MARUTI', 'GVW', 'TN']):
# #                     lob = "CV"
# #                 else:
# #                     lob = "UNKNOWN" 
            
# #             matched_segment = segment_upper
# #             if lob == "BUS":
# #                 if "SCHOOL" not in segment_upper and "STAFF" not in segment_upper:
# #                     matched_segment = "STAFF BUS"
# #                 elif "SCHOOL" in segment_upper:
# #                     matched_segment = "SCHOOL BUS"
# #                 elif "STAFF" in segment_upper:
# #                     matched_segment = "STAFF BUS"
            
# #             matched_rule = None
# #             rule_explanation = ""
# #             company_normalized = company_name.upper().replace('GENERAL', '').replace('INSURANCE', '').strip()
            
# #             for rule in FORMULA_DATA:
# #                 if rule["LOB"] != lob:
# #                     continue
                    
# #                 rule_segment = rule["SEGMENT"].upper()
# #                 segment_match = False
                
# #                 if lob == "CV":
# #                     if "UPTO 2.5" in rule_segment:
# #                         if any(keyword in segment_upper for keyword in ["UPTO 2.5", "2.5 TN", "2.5 GVW", "2.5TN", "2.5GVW", "UPTO2.5"]):
# #                             segment_match = True
# #                     elif "ALL GVW" in rule_segment:
# #                         segment_match = True
# #                 elif lob == "BUS":
# #                     if matched_segment == rule_segment:
# #                         segment_match = True
# #                 elif lob == "PVT CAR":
# #                     if "COMP" in rule_segment and any(keyword in segment for keyword in ["COMP", "COMPREHENSIVE", "PACKAGE", "1ST PARTY", "1+1"]):
# #                         segment_match = True
# #                     elif "TP" in rule_segment and "TP" in segment and "COMP" not in segment:
# #                         segment_match = True
# #                 elif lob == "TW":
# #                     if "1+5" in rule_segment and any(keyword in segment for keyword in ["1+5", "NEW", "FRESH"]):
# #                         segment_match = True
# #                     elif "SAOD + COMP" in rule_segment and any(keyword in segment for keyword in ["SAOD", "COMP", "PACKAGE", "1ST PARTY", "1+1"]):
# #                         segment_match = True
# #                     elif "TP" in rule_segment and "TP" in segment:
# #                         segment_match = True
# #                 else:
# #                     segment_match = True
                
# #                 if not segment_match:
# #                     continue
                
# #                 insurers = [ins.strip().upper() for ins in rule["INSURER"].split(',')]
# #                 company_match = False
                
# #                 if "ALL COMPANIES" in insurers:
# #                     company_match = True
# #                 elif "REST OF COMPANIES" in insurers:
# #                     is_in_specific_list = False
# #                     for other_rule in FORMULA_DATA:
# #                         if (other_rule["LOB"] == rule["LOB"] and 
# #                             other_rule["SEGMENT"] == rule["SEGMENT"] and
# #                             "REST OF COMPANIES" not in other_rule["INSURER"] and
# #                             "ALL COMPANIES" not in other_rule["INSURER"]):
# #                             other_insurers = [ins.strip().upper() for ins in other_rule["INSURER"].split(',')]
# #                             if any(company_key in company_normalized for company_key in other_insurers):
# #                                 is_in_specific_list = True
# #                                 break
# #                     if not is_in_specific_list:
# #                         company_match = True
# #                 else:
# #                     for insurer in insurers:
# #                         if insurer in company_normalized or company_normalized in insurer:
# #                             company_match = True
# #                             break
                
# #                 if not company_match:
# #                     continue
                
# #                 remarks = rule.get("REMARKS", "")
                
# #                 if remarks == "NIL" or "NIL" in remarks.upper():
# #                     matched_rule = rule
# #                     rule_explanation = f"Direct match: LOB={lob}, Segment={rule_segment}, Company={rule['INSURER']}"
# #                     break
# #                 elif any(payin_keyword in remarks for payin_keyword in ["Payin Below", "Payin 21%", "Payin 31%", "Payin Above"]):
# #                     if payin_category in remarks:
# #                         matched_rule = rule
# #                         rule_explanation = f"Payin category match: LOB={lob}, Segment={rule_segment}, Payin={payin_category}"
# #                         break
# #                 else:
# #                     matched_rule = rule
# #                     rule_explanation = f"Other remarks match: LOB={lob}, Segment={rule_segment}, Remarks={remarks}"
# #                     break
            
# #             if matched_rule:
# #                 po_formula = matched_rule["PO"]
# #                 calculated_payout = payin_value
                
# #                 if "90% of Payin" in po_formula:
# #                     calculated_payout *= 0.9
# #                 elif "88% of Payin" in po_formula:
# #                     calculated_payout *= 0.88
# #                 elif "Less 2% of Payin" in po_formula:
# #                     calculated_payout -= 2
# #                 elif "-2%" in po_formula:
# #                     calculated_payout -= 2
# #                 elif "-3%" in po_formula:
# #                     calculated_payout -= 3
# #                 elif "-4%" in po_formula:
# #                     calculated_payout -= 4
# #                 elif "-5%" in po_formula:
# #                     calculated_payout -= 5
                
# #                 calculated_payout = max(0, calculated_payout)
# #                 formula_used = po_formula
# #             else:
# #                 calculated_payout = payin_value
# #                 formula_used = "No matching rule found"
            
# #             result_record = {
# #                 'segment': segment,
# #                 'policy type': record.get('policy type', 'Comp/TP'),
# #                 'location': record.get('location', 'N/A'),
# #                 'payin': f"{payin_value}%",
# #                 'remark': record.get('remark', []),
# #                 'Calculated Payout': f"{calculated_payout:.2f}%",
# #                 'Formula Used': formula_used,
# #                 'Rule Explanation': rule_explanation
# #             }
            
# #             calculated_data.append(result_record)
            
# #         except Exception as e:
# #             logger.error(f"Error processing record: {record}, error: {str(e)}")
# #             result_record = {
# #                 'segment': segment,
# #                 'policy type': record.get('policy type', 'Comp/TP'),
# #                 'location': record.get('location', 'N/A'),
# #                 'payin': f"{payin_value}%",
# #                 'remark': record.get('remark', ['Error']),
# #                 'Calculated Payout': "Error",
# #                 'Formula Used': "Error in calculation",
# #                 'Rule Explanation': f"Error: {str(e)}"
# #             }
# #             calculated_data.append(result_record)
    
# #     return calculated_data

# # def process_files(policy_file_bytes: bytes, policy_filename: str, policy_content_type: str, company_name: str):
# #     """Main processing function with enhanced error handling"""
# #     try:
# #         logger.info("=" * 50)
# #         logger.info(f"🚀 Starting file processing for {policy_filename}...")
# #         logger.info(f"📁 File size: {len(policy_file_bytes)} bytes")
        
# #         # Extract text
# #         logger.info("🔍 Extracting text from policy image...")
# #         extracted_text = extract_text_from_file(policy_file_bytes, policy_filename, policy_content_type)
# #         logger.info(f"✅ Extracted text length: {len(extracted_text)} chars")

# #         if not extracted_text.strip():
# #             logger.error("No text extracted from the image")
# #             raise ValueError("No text could be extracted. Please ensure the image is clear and contains readable text.")

# #         # Parse with AI
# #         logger.info("🧠 Parsing policy data with AI...")
        
# #         # Clean the extracted text before parsing
# #         cleaned_text = clean_json_response(extracted_text)
# #         try:
# #             policy_data = json.loads(cleaned_text)
# #             policy_data = ensure_list_format(policy_data)
            
# #             if not policy_data or len(policy_data) == 0:
# #                 raise ValueError("Parsed data is empty")
                    
# #         except json.JSONDecodeError as e:
# #             logger.error(f"JSON decode error: {str(e)} with cleaned JSON: {cleaned_text[:500]}...")
# #             raise ValueError(f"JSON parsing failed: {str(e)}")
        
# #         logger.info(f"✅ Successfully parsed {len(policy_data)} policy records")

# #         # Classify payin
# #         logger.info("🧮 Classifying payin values...")
# #         for record in policy_data:
# #             try:
# #                 payin_val, payin_cat = classify_payin(record.get('payin', '0%'))
# #                 record['Payin_Value'] = payin_val
# #                 record['Payin_Category'] = payin_cat
# #             except Exception as e:
# #                 logger.warning(f"Error classifying payin: {e}")
# #                 record['Payin_Value'] = 0.0
# #                 record['Payin_Category'] = "Payin Below 20%"

# #         # Apply formulas
# #         logger.info("🧮 Applying formulas and calculating payouts...")
# #         calculated_data = apply_formula_directly(policy_data, company_name)
        
# #         if not calculated_data or len(calculated_data) == 0:
# #             logger.error("No data after formula application")
# #             raise ValueError("No data after formula application")

# #         logger.info(f"✅ Successfully calculated {len(calculated_data)} records")

# #         # Create Excel
# #         logger.info("📊 Creating Excel file...")
# #         df_calc = pd.DataFrame(calculated_data)
        
# #         if df_calc.empty:
# #             logger.error("DataFrame is empty")
# #             raise ValueError("DataFrame is empty")

# #         output = BytesIO()
# #         try:
# #             with pd.ExcelWriter(output, engine='openpyxl') as writer:
# #                 df_calc.to_excel(writer, sheet_name='Policy Data', startrow=2, index=False)
# #                 worksheet = writer.sheets['Policy Data']
# #                 headers = list(df_calc.columns)
# #                 for col_num, value in enumerate(headers, 1):
# #                     cell = worksheet.cell(row=3, column=col_num, value=value)
# #                     cell.font = cell.font.copy(bold=True)
# #                 if len(headers) > 1:
# #                     company_cell = worksheet.cell(row=1, column=1, value=company_name)
# #                     worksheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
# #                     company_cell.font = company_cell.font.copy(bold=True, size=14)
# #                     company_cell.alignment = company_cell.alignment.copy(horizontal='center')
# #                     title_cell = worksheet.cell(row=2, column=1, value='Policy Data with Payin and Calculated Payouts')
# #                     worksheet.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(headers))
# #                     title_cell.font = title_cell.font.copy(bold=True, size=12)
# #                     title_cell.alignment = title_cell.alignment.copy(horizontal='center')
# #                 else:
# #                     worksheet.cell(row=1, column=1, value=company_name)
# #                     worksheet.cell(row=2, column=1, value='Policy Data with Payin and Calculated Payouts')

# #         except Exception as e:
# #             logger.error(f"Error creating Excel file: {str(e)}")
# #             raise ValueError(f"Error creating Excel: {str(e)}")

# #         output.seek(0)
# #         excel_data = output.read()
# #         excel_data_base64 = base64.b64encode(excel_data).decode('utf-8')

# #         # Calculate metrics
# #         avg_payin = sum([r.get('Payin_Value', 0) for r in calculated_data]) / len(calculated_data) if calculated_data else 0.0
# #         unique_segments = len(set([r.get('segment', 'N/A') for r in calculated_data]))
# #         formula_summary = {}
# #         for record in calculated_data:
# #             formula = record.get('Formula Used', 'Unknown')
# #             formula_summary[formula] = formula_summary.get(formula, 0) + 1

# #         logger.info("✅ Processing completed successfully")
# #         logger.info("=" * 50)
        
# #         return {
# #             "extracted_text": extracted_text,
# #             "parsed_data": policy_data,
# #             "calculated_data": calculated_data,
# #             "excel_data": excel_data_base64,
# #             "csv_data": df_calc.to_csv(index=False),
# #             "json_data": json.dumps(calculated_data, indent=2),
# #             "formula_data": FORMULA_DATA,
# #             "metrics": {
# #                 "total_records": len(calculated_data),
# #                 "avg_payin": round(avg_payin, 1),
# #                 "unique_segments": unique_segments,
# #                 "company_name": company_name,
# #                 "formula_summary": formula_summary
# #             }
# #         }

# #     except Exception as e:
# #         logger.error(f"Unexpected error in process_files: {str(e)}", exc_info=True)
# #         raise

# # @app.get("/", response_class=HTMLResponse)
# # async def root():
# #     """Serve a basic HTML frontend or instructions"""
# #     try:
# #         html_path = Path("index.html")
# #         if html_path.exists():
# #             with open(html_path, "r", encoding="utf-8") as f:
# #                 html_content = f.read()
# #             return HTMLResponse(content=html_content)
# #         else:
# #             html_content = """
# #             <h1>Insurance Policy Processing System</h1>
# #             <p>Welcome to the Insurance Policy Processing API.</p>
# #             <h2>Usage Instructions:</h2>
# #             <ul>
# #                 <li><b>Endpoint:</b> POST /process</li>
# #                 <li><b>Parameters:</b>
# #                     <ul>
# #                         <li><b>company_name</b>: String (form-data, required)</li>
# #                         <li><b>policy_file</b>: Image file (PNG, JPG, JPEG, GIF, BMP, TIFF; file upload, required)</li>
# #                     </ul>
# #                 </li>
# #                 <li><b>Response:</b> JSON object containing extracted text, parsed data, calculated data, Excel/CSV/JSON files, and metrics.</li>
# #                 <li><b>Health Check:</b> GET /health</li>
# #             </ul>
# #             <h2>Features:</h2>
# #             <ul>
# #                 <li>AI-powered OCR using GPT-4o for text extraction</li>
# #                 <li>Structured data parsing with detailed remarks</li>
# #                 <li>Payout calculations based on embedded formula rules</li>
# #                 <li>Downloadable Excel, CSV, and JSON outputs</li>
# #             </ul>
# #             """
# #             return HTMLResponse(content=html_content)
# #     except Exception as e:
# #         logger.error(f"Error serving HTML: {str(e)}")
# #         return HTMLResponse(content=f"<h1>Error loading page</h1><p>{str(e)}</p>", status_code=500)

# # @app.post("/process")
# # async def process_policy(company_name: str = Form(...), policy_file: UploadFile = File(...)):
# #     """Process policy image and return extracted and calculated data"""
# #     try:
# #         logger.info("=" * 50)
# #         logger.info(f"📨 Received request for company: {company_name}")
# #         logger.info(f"📄 File: {policy_file.filename}, Content-Type: {policy_file.content_type}")
        
# #         # Read file
# #         policy_file_bytes = await policy_file.read()
# #         if len(policy_file_bytes) == 0:
# #             logger.error("Uploaded file is empty")
# #             return JSONResponse(
# #                 status_code=400,
# #                 content={"error": "Uploaded file is empty"}
# #             )

# #         logger.info(f"📦 File size: {len(policy_file_bytes)} bytes")
        
# #         # Process
# #         results = process_files(
# #             policy_file_bytes, 
# #             policy_file.filename, 
# #             policy_file.content_type,
# #             company_name
# #         )
        
# #         logger.info("✅ Returning results to client")
# #         return JSONResponse(content=results)
        
# #     except ValueError as e:
# #         logger.error(f"Validation error: {str(e)}")
# #         return JSONResponse(
# #             status_code=400,
# #             content={"error": str(e)}
# #         )
# #     except Exception as e:
# #         logger.error(f"Error processing request: {str(e)}", exc_info=True)
# #         return JSONResponse(
# #             status_code=500,
# #             content={"error": f"Processing failed: {str(e)}"}
# #         )

# # @app.get("/health")
# # async def health_check():
# #     """Health check endpoint"""
# #     return JSONResponse(content={"status": "healthy", "message": "Server is running"})

# # if __name__ == "__main__":
# #     import uvicorn
# #     logger.info("🚀 Starting Insurance Policy Processing System...")
# #     logger.info("📡 Server will be available at: http://localhost:8000")
# #     logger.info("🔑 OpenAI API Key is configured: ✅")
# #     uvicorn.run(app, host="0.0.0.0", port=8000)


# from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# from fastapi.responses import JSONResponse, HTMLResponse
# from fastapi.middleware.cors import CORSMiddleware
# from io import BytesIO
# import base64
# import json
# import os
# from dotenv import load_dotenv
# import logging
# import re
# import pandas as pd
# from openai import OpenAI
# from pathlib import Path

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()

# # Load OpenAI API key
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# if not OPENAI_API_KEY:
#     logger.error("⚠️ OPENAI_API_KEY environment variable not set")
#     raise RuntimeError("OPENAI_API_KEY environment variable not set. Please create a .env file with OPENAI_API_KEY=your-key")

# # Initialize OpenAI client
# try:
#     client = OpenAI(api_key=OPENAI_API_KEY)
#     logger.info("✅ OpenAI client initialized successfully")
# except Exception as e:
#     logger.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
#     raise RuntimeError(f"Failed to initialize OpenAI client: {str(e)}")

# app = FastAPI(title="Insurance Policy Processing System")

# # Add CORS middleware for frontend compatibility
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # <-- allow all origins in development (use specific origins in production)
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Embedded Formula Data
# FORMULA_DATA = [
#     {"LOB": "TW", "SEGMENT": "1+5", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "NIL"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "NIL"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-5%", "REMARKS": "Payin Above 50%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Bajaj, Digit, ICICI", "PO": "-3%", "REMARKS": "Payin Above 20%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR COMP + SAOD", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "All Fuel"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Bajaj, Digit, SBI", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Bajaj, Digit, SBI", "PO": "-3%", "REMARKS": "Payin Above 20%"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Rest of Companies", "PO": "90% of Payin", "REMARKS": "Zuno - 21"},
#     {"LOB": "CV", "SEGMENT": "Upto 2.5 GVW", "INSURER": "Reliance, SBI", "PO": "-2%", "REMARKS": "NIL"},
#     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
#     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
#     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
#     {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "INSURER": "TATA, Reliance, Digit, ICICI", "PO": "Less 2% of Payin", "REMARKS": "NIL"},
#     {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "INSURER": "Rest of Companies", "PO": "88% of Payin", "REMARKS": "NIL"},
#     {"LOB": "BUS", "SEGMENT": "STAFF BUS", "INSURER": "All Companies", "PO": "88% of Payin", "REMARKS": "NIL"},
#     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
#     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
#     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
#     {"LOB": "MISD", "SEGMENT": "Misd, Tractor", "INSURER": "All Companies", "PO": "88% of Payin", "REMARKS": "NIL"}
# ]

# def extract_text_from_file(file_bytes: bytes, filename: str, content_type: str) -> str:
#     """Extract text from uploaded image file and structure it into JSON with specified keys"""
#     file_extension = filename.split('.')[-1].lower() if '.' in filename else ''
#     file_type = content_type if content_type else file_extension

#     # Image-based extraction with structured JSON output
#     image_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
#     if file_extension in image_extensions or file_type.startswith('image/'):
#         try:
#             image_base64 = base64.b64encode(file_bytes).decode('utf-8')
            
#             prompt = """
#             Extract the text from the image. Please segregate everything based on the segment, policy type, location, payin, and remark as the keys.
#             Please give me in the JSON format.
#             - payin is in percentage, values in the range of 0 to 100.
#             - Put the rest of the information into the remarks as a list of strings.
#             - Points to remember:
#               - Ignore CD1, CD2 is the payin or payrate.
#               - cluster is the location.
#               - Data can be in table format.
#               - Policy types are SATP (which is TP) and Comp.
#               - Ignore CD1.
#               - Comp and TP columns can have sub-columns like CD1 and CD2, so focus on CD2.
#               - 1+1 means Comp, in TW new, it means TW LOB and 1+5 Segment.
#               - Agency, PB clusters are the locations.
#               - If policy type is not mentioned, consider Comp/TP.
#             - Please identify the Segments when parsing.
#               - For example, if the information is regarding a private car and policy type is TP or third party, then Segment should be PVT CAR TP.
#             - For the provided image, if PCV3w is mentioned, it falls under CV LOB and the segment should be "All GVW & PCV 3W, GCV 3W".
#             - Handle negative percentages (e.g., -68%) by treating them as positive (68%).
#             - Include additional details like minimum premium conditions in remarks.
#             Return ONLY valid JSON array, no markdown formatting.
#             """

#             response = client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=[{
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": prompt},
#                         {"type": "image_url", "image_url": {"url": f"data:image/{file_extension};base64,{image_base64}"}}
#                     ]
#                 }],
#                 temperature=0.0,
#                 max_tokens=4000
#             )
            
#             extracted_text = response.choices[0].message.content.strip()
            
#             # Remove Markdown formatting and ensure valid JSON
#             cleaned_text = re.sub(r'```json\s*|\s*```', '', extracted_text).strip()
#             if not cleaned_text:
#                 logger.error("Cleaned text is empty after removing Markdown")
#                 return "[]"
            
#             # Validate JSON structure
#             try:
#                 json.loads(cleaned_text)
#             except json.JSONDecodeError as e:
#                 logger.error(f"Invalid JSON after cleaning: {str(e)}, raw text: {cleaned_text[:500]}...")
#                 return "[]"
            
#             return cleaned_text
            
#         except Exception as e:
#             logger.error(f"Error in OCR extraction: {str(e)}")
#             return "[]"

#     raise ValueError(f"Unsupported file type for {filename}. Only images are supported.")

# def clean_json_response(response_text: str) -> str:
#     """Clean and extract valid JSON array from OpenAI response"""
#     cleaned = re.sub(r'```json\s*|\s*```', '', response_text).strip()
    
#     start_idx = cleaned.find('[')
#     end_idx = cleaned.rfind(']') + 1 if cleaned.rfind(']') != -1 else len(cleaned)
    
#     if start_idx != -1 and end_idx > start_idx:
#         cleaned = cleaned[start_idx:end_idx]
#     else:
#         logger.warning("No valid JSON array found in response, returning empty array")
#         return "[]"
    
#     if not cleaned.startswith('['):
#         cleaned = '[' + cleaned
#     if not cleaned.endswith(']'):
#         cleaned += ']'
    
#     # Validate JSON
#     try:
#         json.loads(cleaned)
#     except json.JSONDecodeError as e:
#         logger.error(f"Invalid JSON after cleaning: {str(e)}, raw text: {cleaned[:500]}...")
#         return "[]"
    
#     return cleaned

# def ensure_list_format(data) -> list:
#     """Ensure data is in list format"""
#     if isinstance(data, list):
#         return data
#     elif isinstance(data, dict):
#         return [data]
#     else:
#         raise ValueError(f"Expected list or dict, got {type(data)}")

# def classify_payin(payin_str):
#     """Converts Payin string to float and classifies its range"""
#     try:
#         payin_clean = str(payin_str).replace('%', '').replace(' ', '').strip()
        
#         if not payin_clean or payin_clean.upper() == 'N/A':
#             return 0.0, "Payin Below 20%"
        
#         # Handle negative signs as hyphens (convert to positive)
#         payin_clean = payin_clean.replace('-', '')
#         payin_value = float(payin_clean)
        
#         if payin_value <= 20:
#             category = "Payin Below 20%"
#         elif 21 <= payin_value <= 30:
#             category = "Payin 21% to 30%"
#         elif 31 <= payin_value <= 50:
#             category = "Payin 31% to 50%"
#         else:
#             category = "Payin Above 50%"
#         return payin_value, category
#     except (ValueError, TypeError) as e:
#         logger.warning(f"Could not parse payin value: {payin_str}, error: {e}")
#         return 0.0, "Payin Below 20%"

# def apply_formula_directly(policy_data, company_name):
#     """Apply formula rules directly using Python logic with default STAFF BUS for unspecified BUS"""
#     if not policy_data:
#         logger.warning("No policy data to process")
#         return []
    
#     calculated_data = []
    
#     for record in policy_data:
#         try:
#             segment = str(record.get('segment', '')).upper()
#             payin_value = record.get('payin', 0)
#             payin_category = record.get('Payin_Category', '')
            
#             lob = ""
#             segment_upper = segment.upper()
            
#             if any(tw_keyword in segment_upper for tw_keyword in ['TW', '2W', 'TWO WHEELER', 'TWO-WHEELER', 'MCY', 'MC', 'SC']):
#                 lob = "TW"
#             elif any(car_keyword in segment_upper for car_keyword in ['PVT CAR', 'PRIVATE CAR', 'CAR', 'PCI']):
#                 lob = "PVT CAR"
#             elif any(cv_keyword in segment_upper for cv_keyword in ['CV', 'COMMERCIAL', 'LCV', 'GVW', 'TN', 'UPTO', 'ALL GVW', 'PCV', 'GCV']):
#                 lob = "CV"
#             elif 'BUS' in segment_upper:
#                 lob = "BUS"
#             elif 'TAXI' in segment_upper:
#                 lob = "TAXI"
#             elif any(misd_keyword in segment_upper for misd_keyword in ['MISD', 'TRACTOR', 'MISC', 'AMBULANCE', 'POLICE VAN', 'GARBAGE VAN']):
#                 lob = "MISD"
#             else:
#                 remarks_upper = str(record.get('remark', '')).upper() if isinstance(record.get('remark'), str) else ' '.join(record.get('remark', [])).upper()
#                 if any(cv_keyword in remarks_upper for cv_keyword in ['TATA', 'MARUTI', 'GVW', 'TN']):
#                     lob = "CV"
#                 else:
#                     lob = "UNKNOWN" 
            
#             matched_segment = segment_upper
#             if lob == "BUS":
#                 if "SCHOOL" not in segment_upper and "STAFF" not in segment_upper:
#                     matched_segment = "STAFF BUS"
#                 elif "SCHOOL" in segment_upper:
#                     matched_segment = "SCHOOL BUS"
#                 elif "STAFF" in segment_upper:
#                     matched_segment = "STAFF BUS"
            
#             matched_rule = None
#             rule_explanation = ""
#             company_normalized = company_name.upper().replace('GENERAL', '').replace('INSURANCE', '').strip()
            
#             for rule in FORMULA_DATA:
#                 if rule["LOB"] != lob:
#                     continue
                    
#                 rule_segment = rule["SEGMENT"].upper()
#                 segment_match = False
                
#                 if lob == "CV":
#                     if "UPTO 2.5" in rule_segment:
#                         if any(keyword in segment_upper for keyword in ["UPTO 2.5", "2.5 TN", "2.5 GVW", "2.5TN", "2.5GVW", "UPTO2.5"]):
#                             segment_match = True
#                     elif "ALL GVW" in rule_segment:
#                         segment_match = True
#                 elif lob == "BUS":
#                     if matched_segment == rule_segment:
#                         segment_match = True
#                 elif lob == "PVT CAR":
#                     if "COMP" in rule_segment and any(keyword in segment for keyword in ["COMP", "COMPREHENSIVE", "PACKAGE", "1ST PARTY", "1+1"]):
#                         segment_match = True
#                     elif "TP" in rule_segment and "TP" in segment and "COMP" not in segment:
#                         segment_match = True
#                 elif lob == "TW":
#                     if "1+5" in rule_segment and any(keyword in segment for keyword in ["1+5", "NEW", "FRESH"]):
#                         segment_match = True
#                     elif "SAOD + COMP" in rule_segment and any(keyword in segment for keyword in ["SAOD", "COMP", "PACKAGE", "1ST PARTY", "1+1"]):
#                         segment_match = True
#                     elif "TP" in rule_segment and "TP" in segment:
#                         segment_match = True
#                 else:
#                     segment_match = True
                
#                 if not segment_match:
#                     continue
                
#                 insurers = [ins.strip().upper() for ins in rule["INSURER"].split(',')]
#                 company_match = False
                
#                 if "ALL COMPANIES" in insurers:
#                     company_match = True
#                 elif "REST OF COMPANIES" in insurers:
#                     is_in_specific_list = False
#                     for other_rule in FORMULA_DATA:
#                         if (other_rule["LOB"] == rule["LOB"] and 
#                             other_rule["SEGMENT"] == rule["SEGMENT"] and
#                             "REST OF COMPANIES" not in other_rule["INSURER"] and
#                             "ALL COMPANIES" not in other_rule["INSURER"]):
#                             other_insurers = [ins.strip().upper() for ins in other_rule["INSURER"].split(',')]
#                             if any(company_key in company_normalized for company_key in other_insurers):
#                                 is_in_specific_list = True
#                                 break
#                     if not is_in_specific_list:
#                         company_match = True
#                 else:
#                     for insurer in insurers:
#                         if insurer in company_normalized or company_normalized in insurer:
#                             company_match = True
#                             break
                
#                 if not company_match:
#                     continue
                
#                 remarks = rule.get("REMARKS", "")
                
#                 if remarks == "NIL" or "NIL" in remarks.upper():
#                     matched_rule = rule
#                     rule_explanation = f"Direct match: LOB={lob}, Segment={rule_segment}, Company={rule['INSURER']}"
#                     break
#                 elif any(payin_keyword in remarks for payin_keyword in ["Payin Below", "Payin 21%", "Payin 31%", "Payin Above"]):
#                     if payin_category in remarks:
#                         matched_rule = rule
#                         rule_explanation = f"Payin category match: LOB={lob}, Segment={rule_segment}, Payin={payin_category}"
#                         break
#                 else:
#                     matched_rule = rule
#                     rule_explanation = f"Other remarks match: LOB={lob}, Segment={rule_segment}, Remarks={remarks}"
#                     break
            
#             if matched_rule:
#                 po_formula = matched_rule["PO"]
#                 calculated_payout = payin_value
                
#                 if "90% of Payin" in po_formula:
#                     calculated_payout *= 0.9
#                 elif "88% of Payin" in po_formula:
#                     calculated_payout *= 0.88
#                 elif "Less 2% of Payin" in po_formula:
#                     calculated_payout -= 2
#                 elif "-2%" in po_formula:
#                     calculated_payout -= 2
#                 elif "-3%" in po_formula:
#                     calculated_payout -= 3
#                 elif "-4%" in po_formula:
#                     calculated_payout -= 4
#                 elif "-5%" in po_formula:
#                     calculated_payout -= 5
                
#                 calculated_payout = max(0, calculated_payout)
#                 formula_used = po_formula
#             else:
#                 calculated_payout = payin_value
#                 formula_used = "No matching rule found"
            
#             # Ensure remark is a list
#             remark_value = record.get('remark', [])
#             if isinstance(remark_value, str):
#                 remark_value = [remark_value]
            
#             result_record = {
#                 'segment': segment,
#                 'policy type': record.get('policy type', 'Comp/TP'),
#                 'location': record.get('location', 'N/A'),
#                 'payin': f"{payin_value}%",
#                 'remark': remark_value,
#                 'Calculated Payout': f"{calculated_payout:.2f}%",
#                 'Formula Used': formula_used,
#                 'Rule Explanation': rule_explanation
#             }
            
#             calculated_data.append(result_record)
            
#         except Exception as e:
#             logger.error(f"Error processing record: {record}, error: {str(e)}")
#             result_record = {
#                 'segment': segment,
#                 'policy type': record.get('policy type', 'Comp/TP'),
#                 'location': record.get('location', 'N/A'),
#                 'payin': f"{payin_value}%",
#                 'remark': record.get('remark', ['Error']),
#                 'Calculated Payout': "Error",
#                 'Formula Used': "Error in calculation",
#                 'Rule Explanation': f"Error: {str(e)}"
#             }
#             calculated_data.append(result_record)
    
#     return calculated_data

# def process_files(policy_file_bytes: bytes, policy_filename: str, policy_content_type: str, company_name: str):
#     """Main processing function with enhanced error handling"""
#     try:
#         logger.info("=" * 50)
#         logger.info(f"🚀 Starting file processing for {policy_filename}...")
#         logger.info(f"📁 File size: {len(policy_file_bytes)} bytes")
        
#         # Extract text
#         logger.info("🔍 Extracting text from policy image...")
#         extracted_text = extract_text_from_file(policy_file_bytes, policy_filename, policy_content_type)
#         logger.info(f"✅ Extracted text length: {len(extracted_text)} chars")

#         if not extracted_text.strip():
#             logger.error("No text extracted from the image")
#             raise ValueError("No text could be extracted. Please ensure the image is clear and contains readable text.")

#         # Parse with AI
#         logger.info("🧠 Parsing policy data with AI...")
        
#         # Clean the extracted text before parsing
#         cleaned_text = clean_json_response(extracted_text)
#         try:
#             policy_data = json.loads(cleaned_text)
#             policy_data = ensure_list_format(policy_data)
            
#             if not policy_data or len(policy_data) == 0:
#                 raise ValueError("Parsed data is empty")
                    
#         except json.JSONDecodeError as e:
#             logger.error(f"JSON decode error: {str(e)} with cleaned JSON: {cleaned_text[:500]}...")
#             raise ValueError(f"JSON parsing failed: {str(e)}")
        
#         logger.info(f"✅ Successfully parsed {len(policy_data)} policy records")

#         # Classify payin
#         logger.info("🧮 Classifying payin values...")
#         for record in policy_data:
#             try:
#                 payin_val, payin_cat = classify_payin(record.get('payin', '0%'))
#                 record['Payin_Value'] = payin_val
#                 record['Payin_Category'] = payin_cat
#             except Exception as e:
#                 logger.warning(f"Error classifying payin: {e}")
#                 record['Payin_Value'] = 0.0
#                 record['Payin_Category'] = "Payin Below 20%"

#         # Apply formulas
#         logger.info("🧮 Applying formulas and calculating payouts...")
#         calculated_data = apply_formula_directly(policy_data, company_name)
        
#         if not calculated_data or len(calculated_data) == 0:
#             logger.error("No data after formula application")
#             raise ValueError("No data after formula application")

#         logger.info(f"✅ Successfully calculated {len(calculated_data)} records")

#         # Create Excel
#         logger.info("📊 Creating Excel file...")
#         df_calc = pd.DataFrame(calculated_data)
        
#         if df_calc.empty:
#             logger.error("DataFrame is empty")
#             raise ValueError("DataFrame is empty")

#         output = BytesIO()
#         try:
#             with pd.ExcelWriter(output, engine='openpyxl') as writer:
#                 df_calc.to_excel(writer, sheet_name='Policy Data', startrow=2, index=False)
#                 worksheet = writer.sheets['Policy Data']
#                 headers = list(df_calc.columns)
#                 for col_num, value in enumerate(headers, 1):
#                     cell = worksheet.cell(row=3, column=col_num, value=value)
#                     cell.font = cell.font.copy(bold=True)
#                 if len(headers) > 1:
#                     company_cell = worksheet.cell(row=1, column=1, value=company_name)
#                     worksheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
#                     company_cell.font = company_cell.font.copy(bold=True, size=14)
#                     company_cell.alignment = company_cell.alignment.copy(horizontal='center')
#                     title_cell = worksheet.cell(row=2, column=1, value='Policy Data with Payin and Calculated Payouts')
#                     worksheet.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(headers))
#                     title_cell.font = title_cell.font.copy(bold=True, size=12)
#                     title_cell.alignment = title_cell.alignment.copy(horizontal='center')
#                 else:
#                     worksheet.cell(row=1, column=1, value=company_name)
#                     worksheet.cell(row=2, column=1, value='Policy Data with Payin and Calculated Payouts')

#         except Exception as e:
#             logger.error(f"Error creating Excel file: {str(e)}")
#             raise ValueError(f"Error creating Excel: {str(e)}")

#         output.seek(0)
#         excel_data = output.read()
#         excel_data_base64 = base64.b64encode(excel_data).decode('utf-8')

#         # Calculate metrics
#         avg_payin = sum([r.get('Payin_Value', 0) for r in calculated_data]) / len(calculated_data) if calculated_data else 0.0
#         unique_segments = len(set([r.get('segment', 'N/A') for r in calculated_data]))
#         formula_summary = {}
#         for record in calculated_data:
#             formula = record.get('Formula Used', 'Unknown')
#             formula_summary[formula] = formula_summary.get(formula, 0) + 1

#         logger.info("✅ Processing completed successfully")
#         logger.info("=" * 50)
        
#         return {
#             "extracted_text": extracted_text,
#             "parsed_data": policy_data,
#             "calculated_data": calculated_data,
#             "excel_data": excel_data_base64,
#             "csv_data": df_calc.to_csv(index=False),
#             "json_data": json.dumps(calculated_data, indent=2),
#             "formula_data": FORMULA_DATA,
#             "metrics": {
#                 "total_records": len(calculated_data),
#                 "avg_payin": round(avg_payin, 1),
#                 "unique_segments": unique_segments,
#                 "company_name": company_name,
#                 "formula_summary": formula_summary
#             }
#         }

#     except Exception as e:
#         logger.error(f"Unexpected error in process_files: {str(e)}", exc_info=True)
#         raise

# @app.get("/", response_class=HTMLResponse)
# async def root():
#     """Serve a basic HTML frontend or instructions"""
#     try:
#         html_path = Path("index.html")
#         if html_path.exists():
#             with open(html_path, "r", encoding="utf-8") as f:
#                 html_content = f.read()
#             return HTMLResponse(content=html_content)
#         else:
#             html_content = """
#             <h1>Insurance Policy Processing System</h1>
#             <p>Welcome to the Insurance Policy Processing API.</p>
#             <h2>Usage Instructions:</h2>
#             <ul>
#                 <li><b>Endpoint:</b> POST /process</li>
#                 <li><b>Parameters:</b>
#                     <ul>
#                         <li><b>company_name</b>: String (form-data, required)</li>
#                         <li><b>policy_file</b>: Image file (PNG, JPG, JPEG, GIF, BMP, TIFF; file upload, required)</li>
#                     </ul>
#                 </li>
#                 <li><b>Response:</b> JSON object containing extracted text, parsed data, calculated data, Excel/CSV/JSON files, and metrics.</li>
#                 <li><b>Health Check:</b> GET /health</li>
#             </ul>
#             <h2>Features:</h2>
#             <ul>
#                 <li>AI-powered OCR using GPT-4o for text extraction</li>
#                 <li>Structured data parsing with detailed remarks</li>
#                 <li>Payout calculations based on embedded formula rules</li>
#                 <li>Downloadable Excel, CSV, and JSON outputs</li>
#             </ul>
#             """
#             return HTMLResponse(content=html_content)
#     except Exception as e:
#         logger.error(f"Error serving HTML: {str(e)}")
#         return HTMLResponse(content=f"<h1>Error loading page</h1><p>{str(e)}</p>", status_code=500)

# @app.post("/process")
# async def process_policy(company_name: str = Form(...), policy_file: UploadFile = File(...)):
#     """Process policy image and return extracted and calculated data"""
#     try:
#         logger.info("=" * 50)
#         logger.info(f"📨 Received request for company: {company_name}")
#         logger.info(f"📄 File: {policy_file.filename}, Content-Type: {policy_file.content_type}")
        
#         # Read file
#         policy_file_bytes = await policy_file.read()
#         if len(policy_file_bytes) == 0:
#             logger.error("Uploaded file is empty")
#             return JSONResponse(
#                 status_code=400,
#                 content={"error": "Uploaded file is empty"}
#             )

#         logger.info(f"📦 File size: {len(policy_file_bytes)} bytes")
        
#         # Process
#         results = process_files(
#             policy_file_bytes, 
#             policy_file.filename, 
#             policy_file.content_type,
#             company_name
#         )
        
#         logger.info("✅ Returning results to client")
#         return JSONResponse(content=results)
        
#     except ValueError as e:
#         logger.error(f"Validation error: {str(e)}")
#         return JSONResponse(
#             status_code=400,
#             content={"error": str(e)}
#         )
#     except Exception as e:
#         logger.error(f"Error processing request: {str(e)}", exc_info=True)
#         return JSONResponse(
#             status_code=500,
#             content={"error": f"Processing failed: {str(e)}"}
#         )

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return JSONResponse(content={"status": "healthy", "message": "Server is running"})

# if __name__ == "__main__":
#     import uvicorn
#     logger.info("🚀 Starting Insurance Policy Processing System...")
#     logger.info("📡 Server will be available at: http://localhost:8000")
#     logger.info("🔑 OpenAI API Key is configured: ✅")
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# from fastapi.responses import JSONResponse, HTMLResponse
# from fastapi.middleware.cors import CORSMiddleware
# from io import BytesIO
# import base64
# import json
# import os
# from dotenv import load_dotenv
# import logging
# import re
# import pandas as pd
# from openai import OpenAI
# from pathlib import Path

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()

# # Load OpenAI API key
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# if not OPENAI_API_KEY:
#     logger.error("⚠️ OPENAI_API_KEY environment variable not set")
#     raise RuntimeError("OPENAI_API_KEY environment variable not set. Please create a .env file with OPENAI_API_KEY=your-key")

# # Initialize OpenAI client
# try:
#     client = OpenAI(api_key=OPENAI_API_KEY)
#     logger.info("✅ OpenAI client initialized successfully")
# except Exception as e:
#     logger.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
#     raise RuntimeError(f"Failed to initialize OpenAI client: {str(e)}")

# app = FastAPI(title="Insurance Policy Processing System")

# # Add CORS middleware for frontend compatibility
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # <-- allow all origins in development (use specific origins in production)
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Embedded Formula Data
# FORMULA_DATA = [
#     {"LOB": "TW", "SEGMENT": "1+5", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "NIL"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "NIL"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-5%", "REMARKS": "Payin Above 50%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Bajaj, Digit, ICICI", "PO": "-3%", "REMARKS": "Payin Above 20%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": "Rest of Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR COMP + SAOD", "INSURER": "All Companies", "PO": "90% of Payin", "REMARKS": "All Fuel"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Bajaj, Digit, SBI", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Bajaj, Digit, SBI", "PO": "-3%", "REMARKS": "Payin Above 20%"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "Rest of Companies", "PO": "90% of Payin", "REMARKS": "Zuno - 21"},
#     {"LOB": "CV", "SEGMENT": "Upto 2.5 GVW", "INSURER": "Reliance, SBI", "PO": "-2%", "REMARKS": "NIL"},
#     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
#     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
#     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "Rest of Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
#     {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "INSURER": "TATA, Reliance, Digit, ICICI", "PO": "Less 2% of Payin", "REMARKS": "NIL"},
#     {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "INSURER": "Rest of Companies", "PO": "88% of Payin", "REMARKS": "NIL"},
#     {"LOB": "BUS", "SEGMENT": "STAFF BUS", "INSURER": "All Companies", "PO": "88% of Payin", "REMARKS": "NIL"},
#     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
#     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
#     {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "All Companies", "PO": "-5%", "REMARKS": "Payin Above 50%"},
#     {"LOB": "MISD", "SEGMENT": "Misd, Tractor", "INSURER": "All Companies", "PO": "88% of Payin", "REMARKS": "NIL"}
# ]

# def extract_text_from_file(file_bytes: bytes, filename: str, content_type: str) -> str:
#     """Extract text from uploaded image file and structure it into JSON with specified keys"""
#     file_extension = filename.split('.')[-1].lower() if '.' in filename else ''
#     file_type = content_type if content_type else file_extension

#     # Image-based extraction with structured JSON output
#     image_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
#     if file_extension in image_extensions or file_type.startswith('image/'):
#         try:
#             image_base64 = base64.b64encode(file_bytes).decode('utf-8')
            
#             prompt = """
#             Extract the text from the image. Please segregate everything based on the segment, policy type, location, payin, and remark as the keys.
#             Please give me in the JSON format.
#             - payin is in percentage, values in the range of 0 to 100.
#             - Put the rest of the information into the remarks as a list of strings.
#             - Points to remember:
#               - Ignore CD1, CD2 is the payin or payrate.
#               - cluster is the location.
#               - Data can be in table format.
#               - Policy types are SATP (which is TP) and Comp.
#               - Ignore CD1.
#               - Comp and TP columns can have sub-columns like CD1 and CD2, so focus on CD2.
#               - 1+1 means Comp, in TW new, it means TW LOB and 1+5 Segment.
#               - Agency, PB clusters are the locations.
#               - If policy type is not mentioned, consider Comp/TP.
#             - Please identify the Segments when parsing.
#               - For example, if the information is regarding a private car and policy type is TP or third party, then Segment should be PVT CAR TP.
#             - For the provided image, if PCV3w is mentioned, it falls under CV LOB and the segment should be "All GVW & PCV 3W, GCV 3W".
#             - Handle negative percentages (e.g., -68%) by treating them as positive (68%).
#             - Include additional details like minimum premium conditions in remarks.
#             Return ONLY valid JSON array, no markdown formatting.
#             """

#             response = client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=[{
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": prompt},
#                         {"type": "image_url", "image_url": {"url": f"data:image/{file_extension};base64,{image_base64}"}}
#                     ]
#                 }],
#                 temperature=0.0,
#                 max_tokens=4000
#             )
            
#             extracted_text = response.choices[0].message.content.strip()
#             logger.debug(f"Raw extracted text: {extracted_text[:500]}...")  # Debug log
            
#             # Remove Markdown formatting and ensure valid JSON
#             cleaned_text = re.sub(r'```json\s*|\s*```|\s+', '', extracted_text).strip()
#             if not cleaned_text:
#                 logger.error("Cleaned text is empty after removing Markdown")
#                 return "[]"
            
#             # Extract JSON array if present
#             start_idx = cleaned_text.find('[')
#             end_idx = cleaned_text.rfind(']') + 1 if cleaned_text.rfind(']') != -1 else len(cleaned_text)
#             if start_idx != -1 and end_idx > start_idx:
#                 cleaned_text = cleaned_text[start_idx:end_idx]
#             else:
#                 logger.warning("No valid JSON array found in response")
#                 return "[]"
            
#             # Validate JSON
#             try:
#                 json.loads(cleaned_text)
#             except json.JSONDecodeError as e:
#                 logger.error(f"Invalid JSON after cleaning: {str(e)}, raw text: {cleaned_text[:500]}...")
#                 return "[]"
            
#             return cleaned_text
            
#         except Exception as e:
#             logger.error(f"Error in OCR extraction: {str(e)}")
#             return "[]"

#     raise ValueError(f"Unsupported file type for {filename}. Only images are supported.")

# def clean_json_response(response_text: str) -> str:
#     """Clean and extract valid JSON array from OpenAI response"""
#     cleaned = re.sub(r'```json\s*|\s*```|\s+', '', response_text).strip()
    
#     start_idx = cleaned.find('[')
#     end_idx = cleaned.rfind(']') + 1 if cleaned.rfind(']') != -1 else len(cleaned)
    
#     if start_idx != -1 and end_idx > start_idx:
#         cleaned = cleaned[start_idx:end_idx]
#     else:
#         logger.warning("No valid JSON array found in response, returning empty array")
#         return "[]"
    
#     if not cleaned.startswith('['):
#         cleaned = '[' + cleaned
#     if not cleaned.endswith(']'):
#         cleaned += ']'
    
#     # Validate JSON
#     try:
#         json.loads(cleaned)
#     except json.JSONDecodeError as e:
#         logger.error(f"Invalid JSON after cleaning: {str(e)}, raw text: {cleaned[:500]}...")
#         return "[]"
    
#     return cleaned

# def ensure_list_format(data) -> list:
#     """Ensure data is in list format"""
#     if isinstance(data, list):
#         return data
#     elif isinstance(data, dict):
#         return [data]
#     else:
#         raise ValueError(f"Expected list or dict, got {type(data)}")

# def classify_payin(payin_str):
#     """Converts Payin string to float and classifies its range"""
#     try:
#         payin_clean = str(payin_str).replace('%', '').replace(' ', '').strip()
        
#         if not payin_clean or payin_clean.upper() == 'N/A':
#             return 0.0, "Payin Below 20%"
        
#         # Handle negative signs as hyphens (convert to positive)
#         payin_clean = payin_clean.replace('-', '')
#         payin_value = float(payin_clean)
        
#         if payin_value <= 20:
#             category = "Payin Below 20%"
#         elif 21 <= payin_value <= 30:
#             category = "Payin 21% to 30%"
#         elif 31 <= payin_value <= 50:
#             category = "Payin 31% to 50%"
#         else:
#             category = "Payin Above 50%"
#         return payin_value, category
#     except (ValueError, TypeError) as e:
#         logger.warning(f"Could not parse payin value: {payin_str}, error: {e}")
#         return 0.0, "Payin Below 20%"

# def apply_formula_directly(policy_data, company_name):
#     """Apply formula rules directly using Python logic with default STAFF BUS for unspecified BUS"""
#     if not policy_data:
#         logger.warning("No policy data to process")
#         return []
    
#     calculated_data = []
    
#     for record in policy_data:
#         try:
#             segment = str(record.get('segment', '')).upper()
#             payin_value = record.get('payin', 0)
#             payin_category = record.get('Payin_Category', '')
            
#             lob = ""
#             segment_upper = segment.upper()
            
#             if any(tw_keyword in segment_upper for tw_keyword in ['TW', '2W', 'TWO WHEELER', 'TWO-WHEELER', 'MCY', 'MC', 'SC']):
#                 lob = "TW"
#             elif any(car_keyword in segment_upper for car_keyword in ['PVT CAR', 'PRIVATE CAR', 'CAR', 'PCI']):
#                 lob = "PVT CAR"
#             elif any(cv_keyword in segment_upper for cv_keyword in ['CV', 'COMMERCIAL', 'LCV', 'GVW', 'TN', 'UPTO', 'ALL GVW', 'PCV', 'GCV']):
#                 lob = "CV"
#             elif 'BUS' in segment_upper:
#                 lob = "BUS"
#             elif 'TAXI' in segment_upper:
#                 lob = "TAXI"
#             elif any(misd_keyword in segment_upper for misd_keyword in ['MISD', 'TRACTOR', 'MISC', 'AMBULANCE', 'POLICE VAN', 'GARBAGE VAN']):
#                 lob = "MISD"
#             else:
#                 remarks_upper = str(record.get('remark', '')).upper() if isinstance(record.get('remark'), str) else ' '.join(record.get('remark', [])).upper()
#                 if any(cv_keyword in remarks_upper for cv_keyword in ['TATA', 'MARUTI', 'GVW', 'TN']):
#                     lob = "CV"
#                 else:
#                     lob = "UNKNOWN" 
            
#             matched_segment = segment_upper
#             if lob == "BUS":
#                 if "SCHOOL" not in segment_upper and "STAFF" not in segment_upper:
#                     matched_segment = "STAFF BUS"
#                 elif "SCHOOL" in segment_upper:
#                     matched_segment = "SCHOOL BUS"
#                 elif "STAFF" in segment_upper:
#                     matched_segment = "STAFF BUS"
            
#             matched_rule = None
#             rule_explanation = ""
#             company_normalized = company_name.upper().replace('GENERAL', '').replace('INSURANCE', '').strip()
            
#             for rule in FORMULA_DATA:
#                 if rule["LOB"] != lob:
#                     continue
                    
#                 rule_segment = rule["SEGMENT"].upper()
#                 segment_match = False
                
#                 if lob == "CV":
#                     if "UPTO 2.5" in rule_segment:
#                         if any(keyword in segment_upper for keyword in ["UPTO 2.5", "2.5 TN", "2.5 GVW", "2.5TN", "2.5GVW", "UPTO2.5"]):
#                             segment_match = True
#                     elif "ALL GVW" in rule_segment:
#                         segment_match = True
#                 elif lob == "BUS":
#                     if matched_segment == rule_segment:
#                         segment_match = True
#                 elif lob == "PVT CAR":
#                     if "COMP" in rule_segment and any(keyword in segment for keyword in ["COMP", "COMPREHENSIVE", "PACKAGE", "1ST PARTY", "1+1"]):
#                         segment_match = True
#                     elif "TP" in rule_segment and "TP" in segment and "COMP" not in segment:
#                         segment_match = True
#                 elif lob == "TW":
#                     if "1+5" in rule_segment and any(keyword in segment for keyword in ["1+5", "NEW", "FRESH"]):
#                         segment_match = True
#                     elif "SAOD + COMP" in rule_segment and any(keyword in segment for keyword in ["SAOD", "COMP", "PACKAGE", "1ST PARTY", "1+1"]):
#                         segment_match = True
#                     elif "TP" in rule_segment and "TP" in segment:
#                         segment_match = True
#                 else:
#                     segment_match = True
                
#                 if not segment_match:
#                     continue
                
#                 insurers = [ins.strip().upper() for ins in rule["INSURER"].split(',')]
#                 company_match = False
                
#                 if "ALL COMPANIES" in insurers:
#                     company_match = True
#                 elif "REST OF COMPANIES" in insurers:
#                     is_in_specific_list = False
#                     for other_rule in FORMULA_DATA:
#                         if (other_rule["LOB"] == rule["LOB"] and 
#                             other_rule["SEGMENT"] == rule["SEGMENT"] and
#                             "REST OF COMPANIES" not in other_rule["INSURER"] and
#                             "ALL COMPANIES" not in other_rule["INSURER"]):
#                             other_insurers = [ins.strip().upper() for ins in other_rule["INSURER"].split(',')]
#                             if any(company_key in company_normalized for company_key in other_insurers):
#                                 is_in_specific_list = True
#                                 break
#                     if not is_in_specific_list:
#                         company_match = True
#                 else:
#                     for insurer in insurers:
#                         if insurer in company_normalized or company_normalized in insurer:
#                             company_match = True
#                             break
                
#                 if not company_match:
#                     continue
                
#                 remarks = rule.get("REMARKS", "")
                
#                 if remarks == "NIL" or "NIL" in remarks.upper():
#                     matched_rule = rule
#                     rule_explanation = f"Direct match: LOB={lob}, Segment={rule_segment}, Company={rule['INSURER']}"
#                     break
#                 elif any(payin_keyword in remarks for payin_keyword in ["Payin Below", "Payin 21%", "Payin 31%", "Payin Above"]):
#                     if payin_category in remarks:
#                         matched_rule = rule
#                         rule_explanation = f"Payin category match: LOB={lob}, Segment={rule_segment}, Payin={payin_category}"
#                         break
#                 else:
#                     matched_rule = rule
#                     rule_explanation = f"Other remarks match: LOB={lob}, Segment={rule_segment}, Remarks={remarks}"
#                     break
            
#             if matched_rule:
#                 po_formula = matched_rule["PO"]
#                 calculated_payout = payin_value
                
#                 if "90% of Payin" in po_formula:
#                     calculated_payout *= 0.9
#                 elif "88% of Payin" in po_formula:
#                     calculated_payout *= 0.88
#                 elif "Less 2% of Payin" in po_formula:
#                     calculated_payout -= 2
#                 elif "-2%" in po_formula:
#                     calculated_payout -= 2
#                 elif "-3%" in po_formula:
#                     calculated_payout -= 3
#                 elif "-4%" in po_formula:
#                     calculated_payout -= 4
#                 elif "-5%" in po_formula:
#                     calculated_payout -= 5
                
#                 calculated_payout = max(0, calculated_payout)
#                 formula_used = po_formula
#             else:
#                 calculated_payout = payin_value
#                 formula_used = "No matching rule found"
            
#             # Ensure remark is a list
#             remark_value = record.get('remark', [])
#             if isinstance(remark_value, str):
#                 remark_value = [remark_value]
            
#             result_record = {
#                 'segment': segment,
#                 'policy type': record.get('policy type', 'Comp/TP'),
#                 'location': record.get('location', 'N/A'),
#                 'payin': f"{payin_value}%",
#                 'remark': remark_value,
#                 'Calculated Payout': f"{calculated_payout:.2f}%",
#                 'Formula Used': formula_used,
#                 'Rule Explanation': rule_explanation
#             }
            
#             calculated_data.append(result_record)
            
#         except Exception as e:
#             logger.error(f"Error processing record: {record}, error: {str(e)}")
#             result_record = {
#                 'segment': segment,
#                 'policy type': record.get('policy type', 'Comp/TP'),
#                 'location': record.get('location', 'N/A'),
#                 'payin': f"{payin_value}%",
#                 'remark': record.get('remark', ['Error']),
#                 'Calculated Payout': "Error",
#                 'Formula Used': "Error in calculation",
#                 'Rule Explanation': f"Error: {str(e)}"
#             }
#             calculated_data.append(result_record)
    
#     return calculated_data

# def process_files(policy_file_bytes: bytes, policy_filename: str, policy_content_type: str, company_name: str):
#     """Main processing function with enhanced error handling"""
#     try:
#         logger.info("=" * 50)
#         logger.info(f"🚀 Starting file processing for {policy_filename}...")
#         logger.info(f"📁 File size: {len(policy_file_bytes)} bytes")
        
#         # Extract text
#         logger.info("🔍 Extracting text from policy image...")
#         extracted_text = extract_text_from_file(policy_file_bytes, policy_filename, policy_content_type)
#         logger.info(f"✅ Extracted text length: {len(extracted_text)} chars")
#         logger.debug(f"Extracted text: {extracted_text[:500]}...")  # Debug log

#         if not extracted_text.strip():
#             logger.error("No text extracted from the image")
#             raise ValueError("No text could be extracted. Please ensure the image is clear and contains readable text.")

#         # Parse with AI
#         logger.info("🧠 Parsing policy data with AI...")
        
#         # Clean the extracted text before parsing
#         cleaned_text = clean_json_response(extracted_text)
#         logger.debug(f"Cleaned text: {cleaned_text}")  # Debug log
#         try:
#             policy_data = json.loads(cleaned_text)
#             policy_data = ensure_list_format(policy_data)
            
#             if not policy_data or len(policy_data) == 0:
#                 raise ValueError("Parsed data is empty")
                    
#         except json.JSONDecodeError as e:
#             logger.error(f"JSON decode error: {str(e)} with cleaned JSON: {cleaned_text[:500]}...")
#             raise ValueError(f"JSON parsing failed: {str(e)}")
        
#         logger.info(f"✅ Successfully parsed {len(policy_data)} policy records")

#         # Classify payin
#         logger.info("🧮 Classifying payin values...")
#         for record in policy_data:
#             try:
#                 payin_val, payin_cat = classify_payin(record.get('payin', '0%'))
#                 record['Payin_Value'] = payin_val
#                 record['Payin_Category'] = payin_cat
#             except Exception as e:
#                 logger.warning(f"Error classifying payin: {e}")
#                 record['Payin_Value'] = 0.0
#                 record['Payin_Category'] = "Payin Below 20%"

#         # Apply formulas
#         logger.info("🧮 Applying formulas and calculating payouts...")
#         calculated_data = apply_formula_directly(policy_data, company_name)
        
#         if not calculated_data or len(calculated_data) == 0:
#             logger.error("No data after formula application")
#             raise ValueError("No data after formula application")

#         logger.info(f"✅ Successfully calculated {len(calculated_data)} records")

#         # Create Excel
#         logger.info("📊 Creating Excel file...")
#         df_calc = pd.DataFrame(calculated_data)
        
#         if df_calc.empty:
#             logger.error("DataFrame is empty")
#             raise ValueError("DataFrame is empty")

#         output = BytesIO()
#         try:
#             with pd.ExcelWriter(output, engine='openpyxl') as writer:
#                 df_calc.to_excel(writer, sheet_name='Policy Data', startrow=2, index=False)
#                 worksheet = writer.sheets['Policy Data']
#                 headers = list(df_calc.columns)
#                 for col_num, value in enumerate(headers, 1):
#                     cell = worksheet.cell(row=3, column=col_num, value=value)
#                     cell.font = cell.font.copy(bold=True)
#                 if len(headers) > 1:
#                     company_cell = worksheet.cell(row=1, column=1, value=company_name)
#                     worksheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
#                     company_cell.font = company_cell.font.copy(bold=True, size=14)
#                     company_cell.alignment = company_cell.alignment.copy(horizontal='center')
#                     title_cell = worksheet.cell(row=2, column=1, value='Policy Data with Payin and Calculated Payouts')
#                     worksheet.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(headers))
#                     title_cell.font = title_cell.font.copy(bold=True, size=12)
#                     title_cell.alignment = title_cell.alignment.copy(horizontal='center')
#                 else:
#                     worksheet.cell(row=1, column=1, value=company_name)
#                     worksheet.cell(row=2, column=1, value='Policy Data with Payin and Calculated Payouts')

#         except Exception as e:
#             logger.error(f"Error creating Excel file: {str(e)}")
#             raise ValueError(f"Error creating Excel: {str(e)}")

#         output.seek(0)
#         excel_data = output.read()
#         excel_data_base64 = base64.b64encode(excel_data).decode('utf-8')

#         # Calculate metrics
#         avg_payin = sum([r.get('Payin_Value', 0) for r in calculated_data]) / len(calculated_data) if calculated_data else 0.0
#         unique_segments = len(set([r.get('segment', 'N/A') for r in calculated_data]))
#         formula_summary = {}
#         for record in calculated_data:
#             formula = record.get('Formula Used', 'Unknown')
#             formula_summary[formula] = formula_summary.get(formula, 0) + 1

#         logger.info("✅ Processing completed successfully")
#         logger.info("=" * 50)
        
#         return {
#             "extracted_text": extracted_text,
#             "parsed_data": policy_data,
#             "calculated_data": calculated_data,
#             "excel_data": excel_data_base64,
#             "csv_data": df_calc.to_csv(index=False),
#             "json_data": json.dumps(calculated_data, indent=2),
#             "formula_data": FORMULA_DATA,
#             "metrics": {
#                 "total_records": len(calculated_data),
#                 "avg_payin": round(avg_payin, 1),
#                 "unique_segments": unique_segments,
#                 "company_name": company_name,
#                 "formula_summary": formula_summary
#             }
#         }

#     except Exception as e:
#         logger.error(f"Unexpected error in process_files: {str(e)}", exc_info=True)
#         raise

# @app.get("/", response_class=HTMLResponse)
# async def root():
#     """Serve a basic HTML frontend or instructions"""
#     try:
#         html_path = Path("index.html")
#         if html_path.exists():
#             with open(html_path, "r", encoding="utf-8") as f:
#                 html_content = f.read()
#             return HTMLResponse(content=html_content)
#         else:
#             html_content = """
#             <h1>Insurance Policy Processing System</h1>
#             <p>Welcome to the Insurance Policy Processing API.</p>
#             <h2>Usage Instructions:</h2>
#             <ul>
#                 <li><b>Endpoint:</b> POST /process</li>
#                 <li><b>Parameters:</b>
#                     <ul>
#                         <li><b>company_name</b>: String (form-data, required)</li>
#                         <li><b>policy_file</b>: Image file (PNG, JPG, JPEG, GIF, BMP, TIFF; file upload, required)</li>
#                     </ul>
#                 </li>
#                 <li><b>Response:</b> JSON object containing extracted text, parsed data, calculated data, Excel/CSV/JSON files, and metrics.</li>
#                 <li><b>Health Check:</b> GET /health</li>
#             </ul>
#             <h2>Features:</h2>
#             <ul>
#                 <li>AI-powered OCR using GPT-4o for text extraction</li>
#                 <li>Structured data parsing with detailed remarks</li>
#                 <li>Payout calculations based on embedded formula rules</li>
#                 <li>Downloadable Excel, CSV, and JSON outputs</li>
#             </ul>
#             """
#             return HTMLResponse(content=html_content)
#     except Exception as e:
#         logger.error(f"Error serving HTML: {str(e)}")
#         return HTMLResponse(content=f"<h1>Error loading page</h1><p>{str(e)}</p>", status_code=500)

# @app.post("/process")
# async def process_policy(company_name: str = Form(...), policy_file: UploadFile = File(...)):
#     """Process policy image and return extracted and calculated data"""
#     try:
#         logger.info("=" * 50)
#         logger.info(f"📨 Received request for company: {company_name}")
#         logger.info(f"📄 File: {policy_file.filename}, Content-Type: {policy_file.content_type}")
        
#         # Read file
#         policy_file_bytes = await policy_file.read()
#         if len(policy_file_bytes) == 0:
#             logger.error("Uploaded file is empty")
#             return JSONResponse(
#                 status_code=400,
#                 content={"error": "Uploaded file is empty"}
#             )

#         logger.info(f"📦 File size: {len(policy_file_bytes)} bytes")
        
#         # Process
#         results = process_files(
#             policy_file_bytes, 
#             policy_file.filename, 
#             policy_file.content_type,
#             company_name
#         )
        
#         logger.info("✅ Returning results to client")
#         return JSONResponse(content=results)
        
#     except ValueError as e:
#         logger.error(f"Validation error: {str(e)}")
#         return JSONResponse(
#             status_code=400,
#             content={"error": str(e)}
#         )
#     except Exception as e:
#         logger.error(f"Error processing request: {str(e)}", exc_info=True)
#         return JSONResponse(
#             status_code=500,
#             content={"error": f"Processing failed: {str(e)}"}
#         )

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return JSONResponse(content={"status": "healthy", "message": "Server is running"})

# if __name__ == "__main__":
#     import uvicorn
#     logger.info("🚀 Starting Insurance Policy Processing System...")
#     logger.info("📡 Server will be available at: http://localhost:8000")
#     logger.info("🔑 OpenAI API Key is configured: ✅")
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
import base64
import json
import os
from dotenv import load_dotenv
import logging
import re
import pandas as pd
from openai import OpenAI
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("⚠️ OPENAI_API_KEY environment variable not set")
    raise RuntimeError("OPENAI_API_KEY environment variable not set. Please create a .env file with OPENAI_API_KEY=your-key")

# Initialize OpenAI client
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    logger.info("✅ OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
    raise RuntimeError(f"Failed to initialize OpenAI client: {str(e)}")

app = FastAPI(title="Insurance Policy Processing System")

# Add CORS middleware for frontend compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Embedded Formula Data
FORMULA_DATA = [
    {"LOB": "TW", "SEGMENT": "1+5", "INSURER": "DIGIT", "PO": "90% of Payin", "REMARKS": "NIL"},
    {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-2%", "REMARKS": "Payin Below 20%"},
    {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
    {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
    {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "INSURER": "DIGIT", "PO": "-5%", "REMARKS": "Payin Above 50%"},
    {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": " DIGIT", "PO": "-3%", "REMARKS": "Payin Above 20%"},
    {"LOB": "TW", "SEGMENT": "TW TP", "INSURER": " DIGIT", "PO": "23%", "REMARKS": "Payin Below 20%"},
{"LOB": "PVT CAR", "SEGMENT": "PVT CAR COMP + SAOD", "INSURER": "DIGIT", "PO": "90% of Payin", "REMARKS": "All Fuel"},
    {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "DIGIT", "PO": "-2%", "REMARKS": "Payin Below 20%"},
    {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "INSURER": "DIGIT", "PO": "-3%", "REMARKS": "Payin Above 20%"},
    {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "DIGIT", "PO": "-2%", "REMARKS": "Payin Below 20%"},
    {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "DIGIT", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
    {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "DIGIT", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
    {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "INSURER": "DIGIT", "PO": "-5%", "REMARKS": "Payin Above 50%"},
    {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "INSURER": "DIGIT", "PO": "Less 2% of Payin", "REMARKS": "NIL"},
    {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "INSURER": "DIGIT", "PO": "88% of Payin", "REMARKS": "NIL"},
    {"LOB": "BUS", "SEGMENT": "STAFF BUS", "INSURER": "DIGIT", "PO": "88% of Payin", "REMARKS": "NIL"},
    {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "DIGIT", "PO": "-2%", "REMARKS": "Payin Below 20%"},
    {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "DIGIT", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
    {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "DIGIT", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
    {"LOB": "TAXI", "SEGMENT": "TAXI", "INSURER": "DIGIT", "PO": "-5%", "REMARKS": "Payin Above 50%"},
    {"LOB": "MISD", "SEGMENT": "Misd, Tractor", "INSURER": "DIGIT", "PO": "88% of Payin", "REMARKS": "NIL"}
]

def extract_text_from_file(file_bytes: bytes, filename: str, content_type: str) -> str:
    """Extract text from uploaded image file and structure it into JSON with specified keys"""
    file_extension = filename.split('.')[-1].lower() if '.' in filename else ''
    file_type = content_type if content_type else file_extension

    image_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
    if file_extension in image_extensions or file_type.startswith('image/'):
        try:
            image_base64 = base64.b64encode(file_bytes).decode('utf-8')
            
            prompt = """
            Extract the text from the image. Please segregate everything based on the segment, policy_type, location, payin, and remark as the keys.
            
            
            CRITICAL INSTRUCTIONS:
            - payin is in percentage, values in the range of 0 to 100 (as NUMBER, not string)
            - Put the rest of the information into the remarks as a STRING value (not a list) including the segment mentioned in the input file
            - Points to remember:
              - Ignore CD1, CD2 is the payin or payrate
              - cluster is the location
              - Data can be in table format
              - Policy types are SATP (which is TP) and Comp
              - Ignore CD1 completely
              - Comp and TP columns can have sub-columns like CD1 and CD2, so focus on CD2
              - 1+1 means Comp, in TW new it means TW LOB and 1+5 Segment
              - Agency, PB clusters are the locations
              - If policy type is not mentioned, consider Comp/TP
            - Please identify the Segments when parsing and map it to whatever I will give in this prompt in the note section:
              - For example, if the information is regarding a private car and policy type is TP or third party, then Segment should be PVT CAR TP
            - For the provided image, if PCV3w is mentioned, it falls under CV LOB and the segment should be "All GVW & PCV 3W, GCV 3W"
            - Handle negative percentages (e.g., -68%) by treating them as positive (68%)
            - Include additional details like minimum premium conditions in remarks as a single string
            - If GVW is let's say upto 2.5 TN , then segment should be ALL GVW & PCV 3W, GCV 3W as the comapany is Digit so for that , do it 
            Let me help you to map the segment 
            if PCV 3w is mentioned then it comes under the segment of All GVW & PCV 3W, GCV 3W , no matter if GCV and how much tn (ton) is mentioned
            - If the segment is related to two wheelers like MC, MCY, SC, etc., classify it under the "TW" segment. 
            see , if the policy type  of two wheeler is mentioned like Comp or OD or SAOD then please write the segment as TW SAOD + COMP  , if policy type is not mentioned then by default consider it as this only
            if the policy type of two wheeler is mentioned like TP or SATP then please write the segment as TW TP
            if any thing mentioned two wheeler like New or Fresh then the Segment should be 1+5
            - sometimes the data is given in tabular format , so please take care of that too while extracting the data , if 2W it means TW , and in the next column , sub-solumns there where 1+1 means Comp and below it CD2 there
            -SATP means TP policy type 
            -Same for the Private Car too  , if the policy of the Private car is mentioned as SAOD or OD , Comp , then the segment is PVT CAR COMP + SAOD,
            if the policy type mentioned is TP then the segment will be PVT CAR TP


            - if anything related to bus mentioned and if it is school bus then Segment is SCHOOL BUS , if staff bus mentioned then consider it as STAFF BUS segment
            -if taxi is mentioned no matter kaali pilli taxi or whatever taxi , it comes under the segment of TAXI

            -if Tractor, Ambulance, Police Van, Fire Brigade, Misd etc is mentioned then segment is MISD
            
            JSON FORMAT EXAMPLE:
            [
              {
                "segment": "TW SAOD + COMP",
                "policy_type": "Comp",
                "location": "APTS_Good1",
                "payin": 52.5,
                "remark": "MC<=180 Hero/Honda"
              }
            ]
            
            Return ONLY valid JSON array with numeric payin values and string remarks, no markdown formatting.
            """
           
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/{file_extension};base64,{image_base64}"}}
                    ]
                }],
                temperature=0.0,
                max_tokens=4000
            )
            
            extracted_text = response.choices[0].message.content.strip()
            
            # Remove Markdown formatting
            cleaned_text = re.sub(r'```json\s*|\s*```', '', extracted_text).strip()
            if not cleaned_text:
                logger.error("Cleaned text is empty after removing Markdown")
                return "[]"
            
            # Extract JSON array if present
            start_idx = cleaned_text.find('[')
            end_idx = cleaned_text.rfind(']') + 1 if cleaned_text.rfind(']') != -1 else len(cleaned_text)
            if start_idx != -1 and end_idx > start_idx:
                cleaned_text = cleaned_text[start_idx:end_idx]
            else:
                logger.warning("No valid JSON array found in response")
                return "[]"
            
            # Validate JSON
            try:
                json.loads(cleaned_text)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON after cleaning: {str(e)}, raw text: {cleaned_text[:500]}...")
                return "[]"
            
            return cleaned_text
            
        except Exception as e:
            logger.error(f"Error in OCR extraction: {str(e)}")
            return "[]"

    raise ValueError(f"Unsupported file type for {filename}. Only images are supported.")

def clean_json_response(response_text: str) -> str:
    """Clean and extract valid JSON array from OpenAI response"""
    cleaned = re.sub(r'```json\s*|\s*```', '', response_text).strip()
    
    start_idx = cleaned.find('[')
    end_idx = cleaned.rfind(']') + 1 if cleaned.rfind(']') != -1 else len(cleaned)
    
    if start_idx != -1 and end_idx > start_idx:
        cleaned = cleaned[start_idx:end_idx]
    else:
        logger.warning("No valid JSON array found in response, returning empty array")
        return "[]"
    
    if not cleaned.startswith('['):
        cleaned = '[' + cleaned
    if not cleaned.endswith(']'):
        cleaned += ']'
    
    # Validate JSON
    try:
        json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON after cleaning: {str(e)}, raw text: {cleaned[:500]}...")
        return "[]"
    
    return cleaned

def ensure_list_format(data) -> list:
    """Ensure data is in list format"""
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        return [data]
    else:
        raise ValueError(f"Expected list or dict, got {type(data)}")

def classify_payin(payin_value):
    """Converts Payin value to float and classifies its range"""
    try:
        # If already a number, use it directly
        if isinstance(payin_value, (int, float)):
            payin_float = float(payin_value)
        else:
            # If string, clean and convert
            payin_clean = str(payin_value).replace('%', '').replace(' ', '').strip()
            
            if not payin_clean or payin_clean.upper() == 'N/A':
                return 0.0, "Payin Below 20%"
            
            # Handle negative signs as hyphens (convert to positive)
            payin_clean = payin_clean.replace('-', '')
            payin_float = float(payin_clean)
        
        if payin_float <= 20:
            category = "Payin Below 20%"
        elif 21 <= payin_float <= 30:
            category = "Payin 21% to 30%"
        elif 31 <= payin_float <= 50:
            category = "Payin 31% to 50%"
        else:
            category = "Payin Above 50%"
        return payin_float, category
    except (ValueError, TypeError) as e:
        logger.warning(f"Could not parse payin value: {payin_value}, error: {e}")
        return 0.0, "Payin Below 20%"

def apply_formula_directly(policy_data, company_name):
    """Apply formula rules directly using Python logic"""
    if not policy_data:
        logger.warning("No policy data to process")
        return []
    
    calculated_data = []
    
    for record in policy_data:
        try:
            segment = str(record.get('segment', '')).upper()
            # Use Payin_Value which is the numeric value from classify_payin
            payin_value = record.get('Payin_Value', 0)
            payin_category = record.get('Payin_Category', '')
            
            lob = ""
            segment_upper = segment.upper()
            
            # Determine LOB from segment
            if any(tw_keyword in segment_upper for tw_keyword in ['TW', '2W', 'TWO WHEELER', 'TWO-WHEELER', 'MCY', 'MC', 'SC', 'MCTP', 'SC/EVTP']):
                lob = "TW"
            elif any(car_keyword in segment_upper for car_keyword in ['PVT CAR', 'PRIVATE CAR', 'CAR', 'PCI']):
                lob = "PVT CAR"
            elif any(cv_keyword in segment_upper for cv_keyword in ['CV', 'COMMERCIAL', 'LCV', 'GVW', 'TN', 'UPTO', 'ALL GVW', 'PCV', 'GCV']):
                lob = "CV"
            elif 'BUS' in segment_upper:
                lob = "BUS"
            elif 'TAXI' in segment_upper:
                lob = "TAXI"
            elif any(misd_keyword in segment_upper for misd_keyword in ['MISD', 'TRACTOR', 'MISC', 'AMBULANCE', 'POLICE VAN', 'GARBAGE VAN']):
                lob = "MISD"
            else:
                remarks_upper = str(record.get('remark', '')).upper()
                if any(cv_keyword in remarks_upper for cv_keyword in ['TATA', 'MARUTI', 'GVW', 'TN']):
                    lob = "CV"
                else:
                    lob = "UNKNOWN"
            
            matched_segment = segment_upper
            if lob == "BUS":
                if "SCHOOL" not in segment_upper and "STAFF" not in segment_upper:
                    matched_segment = "STAFF BUS"
                elif "SCHOOL" in segment_upper:
                    matched_segment = "SCHOOL BUS"
                elif "STAFF" in segment_upper:
                    matched_segment = "STAFF BUS"
            
            matched_rule = None
            rule_explanation = ""
            company_normalized = company_name.upper().replace('GENERAL', '').replace('INSURANCE', '').strip()
            
            # Find matching formula rule
            for rule in FORMULA_DATA:
                if rule["LOB"] != lob:
                    continue
                    
                rule_segment = rule["SEGMENT"].upper()
                segment_match = False
                
                if lob == "CV":
                    if "UPTO 2.5" in rule_segment:
                        if any(keyword in segment_upper for keyword in ["UPTO 2.5", "2.5 TN", "2.5 GVW", "2.5TN", "2.5GVW", "UPTO2.5"]):
                            segment_match = True
                    elif "ALL GVW" in rule_segment:
                        segment_match = True
                elif lob == "BUS":
                    if matched_segment == rule_segment:
                        segment_match = True
                elif lob == "PVT CAR":
                    if "COMP" in rule_segment and any(keyword in segment for keyword in ["COMP", "COMPREHENSIVE", "PACKAGE", "1ST PARTY", "1+1"]):
                        segment_match = True
                    elif "TP" in rule_segment and "TP" in segment and "COMP" not in segment:
                        segment_match = True
                elif lob == "TW":
                    if "1+5" in rule_segment and any(keyword in segment for keyword in ["1+5", "NEW", "FRESH"]):
                        segment_match = True
                    elif "SAOD + COMP" in rule_segment and any(keyword in segment for keyword in ["SAOD", "COMP", "PACKAGE", "1ST PARTY", "1+1"]):
                        segment_match = True
                    elif "TP" in rule_segment and "TP" in segment:
                        segment_match = True
                else:
                    segment_match = True
                
                if not segment_match:
                    continue
                
                insurers = [ins.strip().upper() for ins in rule["INSURER"].split(',')]
                company_match = False
                
                if "ALL COMPANIES" in insurers:
                    company_match = True
                elif "REST OF COMPANIES" in insurers:
                    is_in_specific_list = False
                    for other_rule in FORMULA_DATA:
                        if (other_rule["LOB"] == rule["LOB"] and 
                            other_rule["SEGMENT"] == rule["SEGMENT"] and
                            "REST OF COMPANIES" not in other_rule["INSURER"] and
                            "ALL COMPANIES" not in other_rule["INSURER"]):
                            other_insurers = [ins.strip().upper() for ins in other_rule["INSURER"].split(',')]
                            if any(company_key in company_normalized for company_key in other_insurers):
                                is_in_specific_list = True
                                break
                    if not is_in_specific_list:
                        company_match = True
                else:
                    for insurer in insurers:
                        if insurer in company_normalized or company_normalized in insurer:
                            company_match = True
                            break
                
                if not company_match:
                    continue
                
                remarks = rule.get("REMARKS", "")
                
                if remarks == "NIL" or "NIL" in remarks.upper():
                    matched_rule = rule
                    rule_explanation = f"Direct match: LOB={lob}, Segment={rule_segment}, Company={rule['INSURER']}"
                    break
                elif any(payin_keyword in remarks for payin_keyword in ["Payin Below", "Payin 21%", "Payin 31%", "Payin Above"]):
                    if payin_category in remarks:
                        matched_rule = rule
                        rule_explanation = f"Payin category match: LOB={lob}, Segment={rule_segment}, Payin={payin_category}"
                        break
                else:
                    matched_rule = rule
                    rule_explanation = f"Other remarks match: LOB={lob}, Segment={rule_segment}, Remarks={remarks}"
                    break
            
            # Calculate payout based on matched rule
            if matched_rule:
                po_formula = matched_rule["PO"]
                calculated_payout = payin_value
                
                if "90% of Payin" in po_formula:
                    calculated_payout *= 0.9
                elif "88% of Payin" in po_formula:
                    calculated_payout *= 0.88
                elif "Less 2% of Payin" in po_formula:
                    calculated_payout -= 2
                elif "-2%" in po_formula:
                    calculated_payout -= 2
                elif "-3%" in po_formula:
                    calculated_payout -= 3
                elif "-4%" in po_formula:
                    calculated_payout -= 4
                elif "-5%" in po_formula:
                    calculated_payout -= 5
                
                calculated_payout = max(0, calculated_payout)
                formula_used = po_formula
            else:
                calculated_payout = payin_value
                formula_used = "No matching rule found"
                rule_explanation = f"No matching rule for LOB={lob}, Segment={segment_upper}"
            
            # Keep remark as a string
            remark_value = record.get('remark', '')
            if isinstance(remark_value, list):
                remark_value = '; '.join(str(r) for r in remark_value)
            
            result_record = {
                'segment': segment,
                'policy type': record.get('policy_type', 'Comp/TP'),
                'location': record.get('location', 'N/A'),
                'payin': f"{payin_value:.2f}%",
                'remark': str(remark_value),
                'Calculated Payout': f"{calculated_payout:.2f}%",
                'Formula Used': formula_used,
                'Rule Explanation': rule_explanation
            }
            
            calculated_data.append(result_record)
            
        except Exception as e:
            logger.error(f"Error processing record: {record}, error: {str(e)}")
            # Fallback values for error case
            segment = str(record.get('segment', 'Unknown'))
            payin_value = record.get('Payin_Value', 0)
            
            result_record = {
                'segment': segment,
                'policy type': record.get('policy_type', 'Comp/TP'),
                'location': record.get('location', 'N/A'),
                'payin': f"{payin_value:.2f}%" if isinstance(payin_value, (int, float)) else str(payin_value),
                'remark': str(record.get('remark', 'Error')),
                'Calculated Payout': "Error",
                'Formula Used': "Error in calculation",
                'Rule Explanation': f"Error: {str(e)}"
            }
            calculated_data.append(result_record)
    
    return calculated_data

def process_files(policy_file_bytes: bytes, policy_filename: str, policy_content_type: str, company_name: str):
    """Main processing function with enhanced error handling"""
    try:
        logger.info("=" * 50)
        logger.info(f"🚀 Starting file processing for {policy_filename}...")
        logger.info(f"📁 File size: {len(policy_file_bytes)} bytes")
        
        # Extract text
        logger.info("🔍 Extracting text from policy image...")
        extracted_text = extract_text_from_file(policy_file_bytes, policy_filename, policy_content_type)
        logger.info(f"✅ Extracted text length: {len(extracted_text)} chars")

        if not extracted_text.strip() or extracted_text == "[]":
            logger.error("No text extracted from the image")
            raise ValueError("No text could be extracted. Please ensure the image is clear and contains readable text.")

        # Parse extracted text
        logger.info("🧠 Parsing policy data...")
        cleaned_text = clean_json_response(extracted_text)
        
        try:
            policy_data = json.loads(cleaned_text)
            policy_data = ensure_list_format(policy_data)
            
            if not policy_data or len(policy_data) == 0:
                raise ValueError("Parsed data is empty")
                    
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)} with cleaned JSON: {cleaned_text[:500]}...")
            raise ValueError(f"JSON parsing failed: {str(e)}")
        
        logger.info(f"✅ Successfully parsed {len(policy_data)} policy records")

        # Classify payin values
        logger.info("🧮 Classifying payin values...")
        for record in policy_data:
            try:
                payin_val, payin_cat = classify_payin(record.get('payin', 0))
                record['Payin_Value'] = payin_val
                record['Payin_Category'] = payin_cat
            except Exception as e:
                logger.warning(f"Error classifying payin for record {record}: {e}")
                record['Payin_Value'] = 0.0
                record['Payin_Category'] = "Payin Below 20%"

        # Apply formulas
        logger.info("🧮 Applying formulas and calculating payouts...")
        calculated_data = apply_formula_directly(policy_data, company_name)
        
        if not calculated_data or len(calculated_data) == 0:
            logger.error("No data after formula application")
            raise ValueError("No data after formula application")

        logger.info(f"✅ Successfully calculated {len(calculated_data)} records")

        # Create Excel
        logger.info("📊 Creating Excel file...")
        df_calc = pd.DataFrame(calculated_data)
        
        if df_calc.empty:
            logger.error("DataFrame is empty")
            raise ValueError("DataFrame is empty")

        output = BytesIO()
        try:
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_calc.to_excel(writer, sheet_name='Policy Data', startrow=2, index=False)
                worksheet = writer.sheets['Policy Data']
                headers = list(df_calc.columns)
                
                # Format headers
                for col_num, value in enumerate(headers, 1):
                    cell = worksheet.cell(row=3, column=col_num, value=value)
                    cell.font = cell.font.copy(bold=True)
                
                # Add company name and title
                if len(headers) > 1:
                    company_cell = worksheet.cell(row=1, column=1, value=company_name)
                    worksheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
                    company_cell.font = company_cell.font.copy(bold=True, size=14)
                    company_cell.alignment = company_cell.alignment.copy(horizontal='center')
                    
                    title_cell = worksheet.cell(row=2, column=1, value='Policy Data with Payin and Calculated Payouts')
                    worksheet.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(headers))
                    title_cell.font = title_cell.font.copy(bold=True, size=12)
                    title_cell.alignment = title_cell.alignment.copy(horizontal='center')
                else:
                    worksheet.cell(row=1, column=1, value=company_name)
                    worksheet.cell(row=2, column=1, value='Policy Data with Payin and Calculated Payouts')

        except Exception as e:
            logger.error(f"Error creating Excel file: {str(e)}")
            raise ValueError(f"Error creating Excel: {str(e)}")

        output.seek(0)
        excel_data = output.read()
        excel_data_base64 = base64.b64encode(excel_data).decode('utf-8')

        # Calculate metrics
        avg_payin = sum([r.get('Payin_Value', 0) for r in policy_data]) / len(policy_data) if policy_data else 0.0
        unique_segments = len(set([r.get('segment', 'N/A') for r in calculated_data]))
        
        formula_summary = {}
        for record in calculated_data:
            formula = record.get('Formula Used', 'Unknown')
            formula_summary[formula] = formula_summary.get(formula, 0) + 1

        logger.info("✅ Processing completed successfully")
        logger.info("=" * 50)
        
        return {
            "extracted_text": extracted_text,
            "parsed_data": policy_data,
            "calculated_data": calculated_data,
            "excel_data": excel_data_base64,
            "csv_data": df_calc.to_csv(index=False),
            "json_data": json.dumps(calculated_data, indent=2),
            "formula_data": FORMULA_DATA,
            "metrics": {
                "total_records": len(calculated_data),
                "avg_payin": round(avg_payin, 1),
                "unique_segments": unique_segments,
                "company_name": company_name,
                "formula_summary": formula_summary
            }
        }

    except Exception as e:
        logger.error(f"Unexpected error in process_files: {str(e)}", exc_info=True)
        raise

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve a basic HTML frontend or instructions"""
    try:
        html_path = Path("index.html")
        if html_path.exists():
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            return HTMLResponse(content=html_content)
        else:
            html_content = """
            <h1>Insurance Policy Processing System</h1>
            <p>Welcome to the Insurance Policy Processing API.</p>
            <h2>Usage Instructions:</h2>
            <ul>
                <li><b>Endpoint:</b> POST /process</li>
                <li><b>Parameters:</b>
                    <ul>
                        <li><b>company_name</b>: String (form-data, required)</li>
                        <li><b>policy_file</b>: Image file (PNG, JPG, JPEG, GIF, BMP, TIFF; file upload, required)</li>
                    </ul>
                </li>
                <li><b>Response:</b> JSON object containing extracted text, parsed data, calculated data, Excel/CSV/JSON files, and metrics.</li>
                <li><b>Health Check:</b> GET /health</li>
            </ul>
            <h2>Features:</h2>
            <ul>
                <li>AI-powered OCR using GPT-4o for text extraction</li>
                <li>Structured data parsing with detailed remarks</li>
                <li>Payout calculations based on embedded formula rules</li>
                <li>Downloadable Excel, CSV, and JSON outputs</li>
            </ul>
            """
            return HTMLResponse(content=html_content)
    except Exception as e:
        logger.error(f"Error serving HTML: {str(e)}")
        return HTMLResponse(content=f"<h1>Error loading page</h1><p>{str(e)}</p>", status_code=500)

@app.post("/process")
async def process_policy(company_name: str = Form(...), policy_file: UploadFile = File(...)):
    """Process policy image and return extracted and calculated data"""
    try:
        logger.info("=" * 50)
        logger.info(f"📨 Received request for company: {company_name}")
        logger.info(f"📄 File: {policy_file.filename}, Content-Type: {policy_file.content_type}")
        
        # Read file
        policy_file_bytes = await policy_file.read()
        if len(policy_file_bytes) == 0:
            logger.error("Uploaded file is empty")
            return JSONResponse(
                status_code=400,
                content={"error": "Uploaded file is empty"}
            )

        logger.info(f"📦 File size: {len(policy_file_bytes)} bytes")
        
        # Process
        results = process_files(
            policy_file_bytes, 
            policy_file.filename, 
            policy_file.content_type,
            company_name
        )
        
        logger.info("✅ Returning results to client")
        return JSONResponse(content=results)
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": f"Processing failed: {str(e)}"}
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={"status": "healthy", "message": "Server is running"})

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting Insurance Policy Processing System...")
    logger.info("📡 Server will be available at: http://localhost:8000")
    logger.info("🔑 OpenAI API Key is configured: ✅")
    uvicorn.run(app, host="0.0.0.0", port=8000)
