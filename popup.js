document.getElementById('scanBtn').addEventListener('click', async () => {
    const btn = document.getElementById('scanBtn');
    const loader = document.getElementById('loader');
    const result = document.getElementById('result');

    // UI Reset
    btn.style.display = 'none';
    loader.style.display = 'block';
    result.style.display = 'none';

    // 1. Get Selected Text
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => window.getSelection().toString()
    }, async (selection) => {
        const text = selection[0]?.result;

        if (!text || text.length < 5) {
            alert("Please select some text first!");
            btn.style.display = 'block';
            loader.style.display = 'none';
            return;
        }

        try {
            // 2. Call Backend
            const response = await fetch("http://127.0.0.1:8000/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();

            // 3. Update UI
            document.getElementById('gsPaper').innerText = `${data.gs_paper} | ${data.subject}`;
            document.getElementById('topic').innerText = data.micro_topic;
            document.getElementById('relevance').innerText = data.relevance;

            // Prelims
            document.getElementById('prelimsQ').innerText = data.prelims.question;
            document.getElementById('prelimsOpts').innerHTML = data.prelims.options.map(opt => 
                `<span class="mcq-opt">${opt}</span>`
            ).join('');
            document.getElementById('prelimsAns').innerText = `Answer: ${data.prelims.answer} (${data.prelims.explanation})`;

            // Mains
            document.getElementById('mainsQ').innerText = data.mains;

            // Show Result
            loader.style.display = 'none';
            result.style.display = 'block';
            btn.style.display = 'block';
            btn.innerText = "Scan Again";

        } catch (error) {
            alert("Error: Ensure Python Backend is running!");
            console.error(error);
            btn.style.display = 'block';
            loader.style.display = 'none';
        }
    });
});