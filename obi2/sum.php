<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sum App · Akhil Ageer</title>
    <style>
        :root {
            color-scheme: light;
            --ink: #172033;
            --muted: #5c6b80;
            --line: #d5deea;
            --paper: #f4f7fb;
            --card: #ffffff;
            --accent: #0f3d73;
            --accent-2: #b8860b;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: "Iowan Old Style", Palatino, "Palatino Linotype", Georgia, serif;
            color: var(--ink);
            background:
                radial-gradient(900px 420px at 10% -10%, #e7eef8 0%, transparent 60%),
                var(--paper);
        }
        main {
            max-width: 680px;
            margin: 48px auto;
            padding: 0 20px 64px;
        }
        header h1 {
            font-size: 2rem;
            line-height: 1.15;
            margin: 0 0 8px;
        }
        header p { margin: 0; color: var(--muted); }
        .byline {
            margin-top: 14px;
            font-family: "Avenir Next", "Segoe UI", sans-serif;
            font-size: 0.92rem;
            letter-spacing: 0.02em;
        }
        .byline strong { color: var(--accent); }
        form, .result {
            margin-top: 28px;
            background: var(--card);
            border: 1px solid var(--line);
            border-top: 4px solid var(--accent);
            border-radius: 14px;
            padding: 22px;
            box-shadow: 0 10px 30px rgba(23, 32, 51, 0.05);
        }
        label {
            display: block;
            margin: 12px 0 6px;
            font-family: "Avenir Next", "Segoe UI", sans-serif;
            font-size: 0.85rem;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px 14px;
            border: 1px solid var(--line);
            border-radius: 8px;
            font-size: 1.05rem;
        }
        input[type="submit"] {
            margin-top: 18px;
            background: var(--accent);
            color: white;
            border: 0;
            border-radius: 999px;
            padding: 12px 22px;
            font-family: "Avenir Next", "Segoe UI", sans-serif;
            font-size: 0.95rem;
            cursor: pointer;
        }
        .result h3 { margin: 0 0 8px; }
        .result p {
            margin: 0;
            font-size: 1.25rem;
        }
        .swatch {
            height: 8px;
            margin-top: 18px;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--accent), var(--accent-2));
        }
    </style>
</head>
<body>
<main>
    <header>
        <h1>Sum of two numbers</h1>
        <p>A small PHP page that sends both values to a Python script and prints the sum.</p>
        <p class="byline">Author: <strong>Akhil Ageer</strong> · CPS 5745 · <?php echo date("l, F j, Y"); ?></p>
        <div class="swatch"></div>
    </header>

    <form method="POST" action="">
        <label for="num1">Number 1</label>
        <input type="text" id="num1" name="num1" inputmode="decimal" value="<?php echo isset($_POST["num1"]) ? htmlspecialchars($_POST["num1"], ENT_QUOTES) : ""; ?>">
        <label for="num2">Number 2</label>
        <input type="text" id="num2" name="num2" inputmode="decimal" value="<?php echo isset($_POST["num2"]) ? htmlspecialchars($_POST["num2"], ENT_QUOTES) : ""; ?>">
        <input type="submit" name="submit" value="Calculate">
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $num1 = $_POST["num1"];
        $num2 = $_POST["num2"];

        $command = "cd " . escapeshellarg(__DIR__) . " && python3 sum.py " . escapeshellarg($num1) . " " . escapeshellarg($num2);
        $output = shell_exec($command);
        if ($output === null) {
            $output = "Error: python3 sum.py did not return output. shell_exec may be disabled on this server.";
        }

        echo "<section class=\"result\">";
        echo "<h3>Result from Python script</h3>";
        echo "<p>" . htmlspecialchars($output) . "</p>";
        echo "</section>";
    }
    ?>
</main>
</body>
</html>
