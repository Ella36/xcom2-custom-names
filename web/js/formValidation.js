window.onload = function () {
    const form = document.getElementById('form');
    form.addEventListener('submit', onFormSubmit);

    // non-empty line counter
    let textArea = document.getElementById("namesTextArea");
    let lineCounter = document.getElementById("lineCount");
    let tomRadioButton = document.getElementById("tom");
    const characterCounterOriginalColor = lineCounter.style.color;
    const countCharacters = () => {
        let maxCharacters = tomRadioButton.checked ? 500 : 429
        let amountOfLines = textArea.value.split(/\r\n|\r|\n/).filter(item => item.trim()).length
        lineCounter.textContent = `${amountOfLines}/${maxCharacters}`;
        // Color
        if (amountOfLines > maxCharacters - 50) {
            lineCounter.style.color = "red";
        } else if (amountOfLines > maxCharacters - 100) {
            lineCounter.style.color = "orange";
        } else {
            lineCounter.style.color = characterCounterOriginalColor;
        }
    };
    textArea.addEventListener("input", countCharacters);
    tomRadioButton.addEventListener("input", countCharacters);
    document.getElementById("dev").addEventListener("input", countCharacters);
}

async function onFormSubmit(event) {
    event.preventDefault();
    console.group('Javascript: Setting input parameters');
    console.log('Button clicked, working...');

    // Text Area Validation
    // No validation, let python handle it

    // Decide on Input and Output name based on radio button
    let textArea = document.getElementById("namesTextArea");
    const amountOfLines = textArea.value.split(/\r\n|\r|\n/).filter(item => item.trim()).length
    let isTomSelected = document.getElementById("tom").checked
    //
    let outputFileName = "Toms.bin"
    let inputFilename = "./data/"
    if (isTomSelected) {
        outputFileName = "Toms.bin"
        inputFilename += "Toms500.bin";
    }
    else { // Dev selected
        outputFileName = "Dev.bin"
        inputFilename += "Dev429.bin";
    }
    console.log(`Amount of Names: ${amountOfLines}`);
    console.log(`Input bin: ${inputFilename}`);
    console.log(`Output bin: ${outputFileName}`);
    console.groupEnd('Javascript: Setting input parameters');

    // Load script
    const pythonScriptPath = "./web/python/script.py";
    const script = await (await fetch(pythonScriptPath)).text();

    // Load input bin
    blob = await (await fetch(inputFilename)).blob();
    const arrayBuffer = await blob.arrayBuffer();
    input_bin = arrayBuffer

    try {
        console.log(`Loading Pyodide...`);
        // Load Pyodide
        let pyodide = await loadPyodide();
        // Run script
        console.log(`Running Python script`);
        await pyodide.runPythonAsync(script);
        // Read result
        let file = pyodide.FS.readFile("/output.bin");

        // Write result
        const blob = new Blob([file], { type: "application/octet-stream" });
        const url = URL.createObjectURL(blob);

        // Create a link to trigger the download
        const link = document.createElement("a");
        link.href = url;
        link.download = outputFileName;

        // Click the link to trigger the download
        link.click();

        // Release the object URL
        URL.revokeObjectURL(url);
    }
    catch (err) {
        console.log(err);
    }
}
