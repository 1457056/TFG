isOn = true
isOn2 = true
isOn3 = true
document.addEventListener("DOMContentLoaded", () => {
    // Escuchamos el click del botón
// Escuchamos el click del botón
    $('#download').on("click", () => {
        const $elementoParaConvertir = document.body; // <-- Aquí puedes elegir cualquier elemento del DOM
        html2pdf()
            .set({
                margin: 1,
                filename: 'resultados.pdf',
                image: {
                    type: 'png',
                    quality: 0.98
                },
                html2canvas: {
                    scale: 4, // A mayor escala, mejores gráficos, pero más peso
                    letterRendering: true,
                },
                jsPDF: {
                    unit: "in",
                    format: "a1",
                    orientation: 'portrait' // landscape o portrait
                }
            })
            .from($elementoParaConvertir)
            .save()
            .catch(err => console.log(err));
    });
    $('#flexCheckDefault').on("click", () => {

        if (isOn === true) {

            $('#dates').html('<div className="row_date mt-1"><input type="text" name="number" placeholder="Numero de posts" required' +
                'onInvalid="this.setCustomValidity(\'Ingresa un número de posts a analizar\')" >' +
                '<input type="date" id="start" name="start"><input type="date" id="end" name="end"></div>');
            isOn = false;
        } else {
            $('#dates').html('');
            isOn = true;
        }
    });

    $('#flexCheckDefault_fb').on("click", () => {

        if (isOn2 === true) {

            $('#data').html('<input type="text" name="number" placeholder="Numero de páginas" required oninvalid= ' + '"this.setCustomValidity' + "('Ingresa un número de posts a analizar')" + '"' + ' pattern="{1,25})"> '
            );
            isOn2 = false;
        } else {
            $('#data').html('');
            isOn2 = true;
        }
    });
    $('#hideTable').on("click", () => {

        if ($('#table_tw').is(':visible')) {
            console.log('hola')
            $('#table_tw').hide();
            $('#card_tw').show();
        } else {
            $('#table_tw').show();
            $('#card_tw').hide();
        }
    });

    function changeColor() {
        $('#taula_resultats tr').each(function () {
            $(this).find('#rate').each(function () {
                if (($(this)[0].innerHTML) < -0.5) {
                    $(this).css("background-color", "lightcoral");
                } else if ((($(this)[0].innerHTML) >= -0.5) && ((($(this)[0].innerHTML) <= 0.5))) {
                    $(this).css("background-color", "lightblue");
                } else {
                    $(this).css("background-color", "lightgreen");
                }
            })
        });
    }

    changeColor();

});


function changeFB(id) {
    if (id == 1) {
        document.getElementById('image_graph').src = "static/images/fb_images/graphics/circular_graph0.png"
        document.getElementById('image_wordcloud').src = "static/images/fb_images/wordclouds/wordcloud0.jpg"
    }

    if (id == 2) {
        document.getElementById('image_graph').src = "static/images/fb_images/graphics/circular_graph1.png"
        document.getElementById('image_wordcloud').src = "static/images/fb_images/wordclouds/wordcloud1.jpg"
    }
    if (id == 3) {
        document.getElementById('image_graph').src = "static/images/fb_images/graphics/circular_graph2.png"
        document.getElementById('image_wordcloud').src = "static/images/fb_images/wordclouds/wordcloud2.jpg"
    }
    if (id == 4) {
        document.getElementById('image_graph').src = "static/images/fb_images/graphics/circular_graph3.png"
        document.getElementById('image_wordcloud').src = "static/images/fb_images/wordclouds/wordcloud3.jpg"
    }
}


