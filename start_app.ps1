# Start Backend
Write-Host "Starting Backend..."
cd backend
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
cd ..

# Start Frontend
Write-Host "Starting Frontend..."
cd frontend
Start-Process -NoNewWindow -FilePath "npm" -ArgumentList "run dev"
cd ..

Write-Host "Project is running!"
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:5173"
