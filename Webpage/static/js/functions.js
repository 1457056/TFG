isOn = true
document.addEventListener("DOMContentLoaded", () => {
    // Escuchamos el click del botón
    const $advOptions = document.querySelector("#flexCheckDefault");
    $advOptions.addEventListener("click", () => {

        if (isOn === true) {
            document.getElementById('dates').innerHTML = '<div className="row_date mt-1"><input type="text" name="number" placeholder="Numero de posts" required  ' +
                'onInvalid="this.setCustomValidity(\'Ingresa un número de posts a analizar\')" pattern="(?:[0-9]{1,2}|100)$">' +
                '<input type="date" id="start" name="start"><input type="date" id="end" name="end"></div>';
            isOn = false;
        } else {
            document.getElementById('dates').innerHTML = '';
            isOn = true;
        }
    })
    const $boton = document.querySelector("#download");
    $boton.addEventListener("click", () => {
        const $elementoParaConvertir = document.body; // <-- Aquí puedes elegir cualquier elemento del DOM
        html2pdf()
            .set({
                margin: 1,
                filename: 'resultados.pdf',
                image: {
                    type: 'jpeg',
                    quality: 0.98
                },
                html2canvas: {
                    scale: 3, // A mayor escala, mejores gráficos, pero más peso
                    letterRendering: true,
                },
                jsPDF: {
                    unit: "in",
                    format: "a3",
                    orientation: 'portrait' // landscape o portrait
                }
            })
            .from($elementoParaConvertir)
            .save()
            .catch(err => console.log(err));
    });
});



