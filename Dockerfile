FROM python:3.11-slim

#set working directory inside container
WORKDIR /app    

#Copy requirements files and install dependecies
COPY requirements.txt .
RUN pip install -r requirements.txt

#Copy rest of code into container
COPY . .

#Expose port 5000 (Flask default)
EXPOSE 5000

#Run Flask App
CMD ["python", "backend/app.py"]


