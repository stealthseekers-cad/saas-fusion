<script>
  let problemText = '';
  let report = null;
  let isLoading = false;
  let errorMessage = '';

  async function handleSubmit() {
    if (!problemText) {
      errorMessage = 'Please enter a problem description.';
      report = null;
      return;
    }

    isLoading = true;
    errorMessage = '';
    report = null;

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: problemText }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'An unknown server error occurred.');
      }

      const data = await response.json();
      console.log('Data received from backend:', data);
      report = data;

    } catch (error) {
      errorMessage = `Error: ${error.message}`;
      console.error(error);
    } finally {
      isLoading = false;
    }
  }
</script>
