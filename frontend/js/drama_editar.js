console.log(location.search) // lee los argumentos pasados a este formulario
var id=location.search.substr(4)
console.log(id)
const { createApp } = Vue
    createApp({
        data() {
            return {
                id:0,
                titulo:"",
                episodios:0,
                genero:"",
                autor:"",
                imagen:"",
                anio:0,
                estrellas:0,
                descripcion:"",
                url:'https://astorniolo.pythonanywhere.com/dramas/'+id,
            }
        },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    this.id=data.id
                    this.titulo=data.titulo,
                    this.episodios=data.episodios,
                    this.genero=data.genero,
                    this.autor=data.autor,
                    this.anio=data.anio,
                    this.estrellas=data.estrellas,
                    this.descripcion=data.descripcion,
                    this.imagen=data.imagen
                })
                .catch(err => {
                    console.error(err);
                     this.error=true
                })
        },
        modificar() {
            let drama = {
                titulo:this.titulo,
                episodios:this.episodios,
                genero:this.genero,
                autor:this.autor,
                imagen:this.imagen,
                anio:this.anio,
                estrellas:this.estrellas,
                descripcion:this.descripcion
            }
            var options = {
                body: JSON.stringify(drama),
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            }
            fetch(this.url, options)
                .then(function () {
                    alert("Registro modificado")
                    window.location.href = "./dramas.html";
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Modificar")
                })
        }
    },
    created() {
        this.fetchData(this.url)
    },
}).mount('#app')