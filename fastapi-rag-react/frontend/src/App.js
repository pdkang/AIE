import React, { useState } from 'react';
import { 
  Container, 
  Typography, 
  Button, 
  TextField, 
  Box,
  Paper
} from '@mui/material';

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [sessionId, setSessionId] = useState('');
  const [error, setError] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileUpload = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', event.target.files[0]);
    setError('');
    setIsProcessing(true);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json'
        }
      });
      const data = await response.json();
      if (data.session_id) {
        setSessionId(data.session_id);
        console.log('Upload successful, session ID:', data.session_id);
      } else {
        setError('Upload failed: No session ID received');
        console.error('Upload response:', data);
      }
    } catch (error) {
      setError('Upload failed: ' + error.message);
      console.error('Upload error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleQuestionSubmit = async () => {
    if (!sessionId) {
      setError('Please upload a document first');
      return;
    }
    setError('');
    setResponse(''); // Clear previous response

    try {
      console.log('Sending query with session ID:', sessionId);
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          query: question
        }),
      });
      
      console.log('Response status:', response.status);
      const responseText = await response.text();
      console.log('Raw response:', responseText);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, body: ${responseText}`);
      }
      
      const data = JSON.parse(responseText);
      console.log('Parsed response data:', data);
      
      if (data.answer) {
        console.log('Setting response:', data.answer);
        setResponse(data.answer);
        console.log('Response state after setting:', data.answer);
      } else {
        setError('No answer received from the server');
        console.error('Unexpected response format:', data);
      }
    } catch (error) {
      setError('Query failed: ' + error.message);
      console.error('Query error:', error);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          RAG Application
        </Typography>
        
        <Paper sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            Upload Document
          </Typography>
          <Button
            variant="contained"
            component="label"
            disabled={isProcessing}
          >
            {isProcessing ? 'Processing...' : 'Choose File'}
            <input
              type="file"
              hidden
              onChange={handleFileUpload}
              disabled={isProcessing}
            />
          </Button>
          <Typography sx={{ mt: 1, color: isProcessing ? 'info.main' : 'success.main' }}>
            {isProcessing ? 'Processing document...' : 
             sessionId ? 'Document uploaded and processed successfully!' : 
             'No document uploaded yet'}
          </Typography>
        </Paper>

        <Paper sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            Ask a Question
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={2}
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            sx={{ mb: 2 }}
            placeholder="Enter your question here..."
          />
          <Button 
            variant="contained" 
            onClick={handleQuestionSubmit}
            disabled={!sessionId || isProcessing}
          >
            Submit Query
          </Button>
        </Paper>

        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Response
          </Typography>
          
          <Box sx={{ mb: 2 }}>
            {error && (
              <Typography sx={{ color: 'error.main', mb: 2 }}>
                {error}
              </Typography>
            )}
            
            <Typography sx={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
              {response || "No response yet. Please upload a document and ask a question."}
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}

export default App; 