import express from "express"
import predictionRouter from "./src/GET_DATA.js"

const app = express()
const PORT = 8000 

app.use(express.json())
app.use(predictionRouter)

app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`)
})
