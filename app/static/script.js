async function predictPneumonia() {
    const recordId = document.getElementById('recordId').value;
    const resultDiv = document.getElementById('result');
    
    resultDiv.innerHTML = '🤖 AI가 열심히 엑스레이를 분석 중입니다... 잠시만 기다려주세요!';

    try {
        const response = await fetch(/api/medical-records//predict-pneumonia, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (data.success) {
            const isPneumonia = data.data.is_pneumonia ? '폐렴 의심 (O)' : '정상 (X)';
            const confidence = (data.data.confidence * 100).toFixed(1);
            
            resultDiv.innerHTML = 
                <p style='color: green;'>✅ 분석 완료!</p>
                <p>결과: <strong></strong></p>
                <p>정확도: <strong>%</strong></p>
            ;
        } else {
            resultDiv.innerHTML = '<p style=\'color: red;\'>❌ 분석에 실패했습니다.</p>';
        }
    } catch (error) {
        resultDiv.innerHTML = <p style='color: red;'>에러 발생: </p>;
    }
}
