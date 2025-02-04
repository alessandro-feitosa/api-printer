# api-printer

This API receives a PDF or TXT file and a validation token.
It validates the token and saves the file in the files folder.
It sends the file to be printed. If the file is a PDF, it goes to a printer, otherwise it sends it to another printer.
After printing is complete, the file is deleted from the files folder. 

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/alessandro-feitosa/api-printer.git
```
2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Set the environment variable**
```
export SECRET_KEY="your_secret_key"
```
4. **Run the application**
```
python app.py
```
5. **API Endpoint**
```
/upload:
- Method: POST
- Requires:
  - Authorization header with Bearer token
  - File upload field
- Returns:
  - JSON response indicating success or failure.
```
