import express from "express";
import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const router = express.Router();

const currentFile = fileURLToPath(import.meta.url);
const currentDirectory = path.dirname(currentFile);
const projectRoot = path.resolve(currentDirectory, "../..");
const predictionScript = path.join(projectRoot, "predict.py");
const pythonCommand = process.env.PYTHON_COMMAND || "python";

function runPrediction(transaction) {
  return new Promise((resolve, reject) => {
    const python = spawn(pythonCommand, [predictionScript], {
      cwd: projectRoot, // currently in which directory
    });

    let output = ""; // This will store everything Python writes to stdout.
    let errorOutput = ""; // this stores whatever Python writes to stderr.
    let settled = false; // 

    const finishWithError = (error) => {
      if (settled) return;


      settled = true;
      reject(error);
    };
    
    python.stdout.on("data", (chunk) => {
      output += chunk.toString();
    });

    python.stderr.on("data", (chunk) => {
      errorOutput += chunk.toString();
    });

    python.on("error", (error) => {
      finishWithError(new Error(`Could not start Python: ${error.message}`));
    });

    python.on("close", (exitCode) => {
      if (settled) return;

      if (exitCode !== 0) {
        finishWithError(
          new Error(errorOutput.trim() || `Python exited with code ${exitCode}`),
        );
        return;
      }

    //   When the Python process completely finishes:

    // If the Promise has already been handled,
    //     do nothing.

    // Otherwise,
    //     check the exit code.

    // If the exit code is not 0,

    //     if Python printed an error,
    //         reject the Promise with that error.

    //     otherwise,
    //         reject the Promise with a generic message.

    //     stop executing this callback.

      try {
        settled = true;
        resolve(JSON.parse(output));
      } catch (error) {
        finishWithError(new Error(`Python returned invalid JSON: ${error.message}`));
      }
    });

    python.stdin.on("error", (error) => {
      finishWithError(new Error(`Could not send data to Python: ${error.message}`));
    });

    python.stdin.write(JSON.stringify(transaction));
    python.stdin.end();
  });
}

router.post("/predict_fraud", async (req, res) => {
  if (!req.body || typeof req.body !== "object" || Array.isArray(req.body)) {
    return res.status(400).json({
      error: "Request body must be a JSON object containing one transaction.",
    });
  }

  try {
    const prediction = await runPrediction(req.body);
    return res.json(prediction);
  } catch (error) {
    console.error("Prediction request failed:", error.message);
    return res.status(500).json({ error: error.message });
  }
});

export default router;
