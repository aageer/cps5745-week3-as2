<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>WCAG Contrast Ratio · Akhil Ageer</title>
    <style>
        :root {
            color-scheme: light;
            --ink: #1c1915;
            --muted: #6b6256;
            --line: #e4d8c4;
            --paper: #fbf6ee;
            --card: #fffdf9;
            --accent: #6b3f1d;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: "Avenir Next", "Segoe UI", sans-serif;
            color: var(--ink);
            background: var(--paper);
        }
        main { max-width: 760px; margin: 40px auto; padding: 0 20px 72px; }
        h1 {
            font-family: "Iowan Old Style", Palatino, Georgia, serif;
            font-size: 2.15rem;
            line-height: 1.12;
            margin: 0 0 10px;
        }
        .lede { color: var(--muted); max-width: 62ch; }
        .meta { margin-top: 12px; font-size: 0.92rem; }
        form, .result {
            margin-top: 24px;
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 20px;
        }
        .pair { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
        label { display: block; font-size: 0.8rem; margin-bottom: 6px; }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid var(--line);
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        }
        button {
            margin-top: 16px;
            background: var(--accent);
            color: white;
            border: 0;
            border-radius: 999px;
            padding: 12px 18px;
            cursor: pointer;
        }
        .preview {
            margin-top: 16px;
            border-radius: 12px;
            min-height: 92px;
            display: grid;
            place-items: center;
            font-size: 1.35rem;
            font-weight: 650;
        }
        @media (max-width: 640px) { .pair { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
<main>
    <header>
        <h1>WCAG contrast ratio</h1>
        <p class="lede">This page computes the WCAG 2 relative-luminance contrast ratio between a text color and a background color. The formula runs in Python on obi2; this PHP page is only the form.</p>
        <p class="meta">Author of the code: <strong>Akhil Ageer</strong> · CPS 5745 · <?php echo date("l, F j, Y"); ?></p>
    </header>

    <?php
    $text = isset($_POST["text"]) ? $_POST["text"] : "F4E7C5";
    $background = isset($_POST["background"]) ? $_POST["background"] : "1F3A2E";
    $output = "";
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $command = "cd " . escapeshellarg(__DIR__) . " && python3 contrast.py " . escapeshellarg($text) . " " . escapeshellarg($background);
        $output = shell_exec($command);
        if ($output === null) {
            $output = "Error: python3 contrast.py did not return output.";
        }
    }
    $text_css = htmlspecialchars(ltrim($text, "#"), ENT_QUOTES);
    $bg_css = htmlspecialchars(ltrim($background, "#"), ENT_QUOTES);
    ?>

    <form method="POST" action="">
        <div class="pair">
            <div>
                <label for="text">Text color (hex)</label>
                <input type="text" id="text" name="text" value="<?php echo htmlspecialchars($text, ENT_QUOTES); ?>">
            </div>
            <div>
                <label for="background">Background color (hex)</label>
                <input type="text" id="background" name="background" value="<?php echo htmlspecialchars($background, ENT_QUOTES); ?>">
            </div>
        </div>
        <button type="submit" name="submit" value="Calculate">Calculate contrast</button>
        <div class="preview" style="color:#<?php echo $text_css; ?>;background:#<?php echo $bg_css; ?>;">
            Akhil Ageer · sample text
        </div>
    </form>

    <?php if ($output !== "") { ?>
        <section class="result">
            <h2>Result from Python script</h2>
            <p><?php echo htmlspecialchars($output); ?></p>
        </section>
    <?php } ?>
</main>
</body>
</html>
