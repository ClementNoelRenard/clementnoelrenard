<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Snake Game - Écran tactile</title>
  <style>
    body {
      background-color: #eee;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
    }
    canvas {
      border: 1px solid #000;
      background-color: rgb(255, 255, 200);
      touch-action: none; /* Empêche le comportement par défaut du navigateur */
    }
  </style>
</head>
<body>
  <canvas id="game" width="300" height="300"></canvas>
  <script>
    // Configuration du jeu
    const WIDTH = 300;
    const HEIGHT = 300;
    const GRID_SIZE = 15;
    const COLS = WIDTH / GRID_SIZE;
    const ROWS = HEIGHT / GRID_SIZE;

    const WHITE = "rgb(255,255,200)";
    const GREEN = "rgb(0,255,0)";
    const RED = "rgb(255,0,0)";

    const canvas = document.getElementById("game");
    const ctx = canvas.getContext("2d");

    // Fonction pour placer la nourriture à une position aléatoire où le serpent n'est pas présent
    function placeFood(snake) {
      let x, y, conflit;
      do {
        x = Math.floor(Math.random() * COLS);
        y = Math.floor(Math.random() * ROWS);
        conflit = snake.some(segment => segment.x === x && segment.y === y);
      } while (conflit);
      return { x, y };
    }

    // Initialisation du serpent, de la direction, de la nourriture et du score
    let snake = [{ x: Math.floor(COLS / 2), y: Math.floor(ROWS / 2) }];
    let direction = { x: 1, y: 0 }; // Direction initiale vers la droite
    let food = placeFood(snake);
    let score = 0;
    let gameOver = false;

    // Gestion des touches clavier
    document.addEventListener("keydown", (e) => {
      switch (e.key) {
        case "ArrowLeft":
          if (direction.x !== 1) direction = { x: -1, y: 0 };
          break;
        case "ArrowRight":
          if (direction.x !== -1) direction = { x: 1, y: 0 };
          break;
        case "ArrowUp":
          if (direction.y !== 1) direction = { x: 0, y: -1 };
          break;
        case "ArrowDown":
          if (direction.y !== -1) direction = { x: 0, y: 1 };
          break;
      }
    });

    // Variables pour la détection tactile
    let touchStartX = null;
    let touchStartY = null;

    // Gestion du début du geste tactile
    canvas.addEventListener("touchstart", (e) => {
      const touch = e.touches[0];
      touchStartX = touch.pageX;
      touchStartY = touch.pageY;
    });

    // Gestion de la fin du geste tactile
    canvas.addEventListener("touchend", (e) => {
      if (touchStartX === null || touchStartY === null) return;

      const touch = e.changedTouches[0];
      const diffX = touch.pageX - touchStartX;
      const diffY = touch.pageY - touchStartY;

      // Déterminer la direction du swipe
      if (Math.abs(diffX) > Math.abs(diffY)) {
        // Geste horizontal
        if (diffX > 0 && direction.x !== -1) {
          direction = { x: 1, y: 0 };
        } else if (diffX < 0 && direction.x !== 1) {
          direction = { x: -1, y: 0 };
        }
      } else {
        // Geste vertical
        if (diffY > 0 && direction.y !== -1) {
          direction = { x: 0, y: 1 };
        } else if (diffY < 0 && direction.y !== 1) {
          direction = { x: 0, y: -1 };
        }
      }

      // Réinitialiser les valeurs de départ
      touchStartX = null;
      touchStartY = null;
    });

    // Fonction principale de mise à jour du jeu
    function update() {
      if (gameOver) return;

      // Calcul de la nouvelle tête du serpent
      const head = snake[0];
      const newHead = { x: head.x + direction.x, y: head.y + direction.y };

      // Collision avec les bords
      if (newHead.x < 0 || newHead.x >= COLS || newHead.y < 0 || newHead.y >= ROWS) {
        gameOver = true;
        drawGame();
        gameOverScreen();
        return;
      }

      // Vérification de l'aliment mangé
      const ateFood = newHead.x === food.x && newHead.y === food.y;
      if (ateFood) {
        score++;
        food = placeFood(snake);
      } else {
        snake.pop(); // Enlever la queue si aucun aliment n'est mangé
      }

      // Ajout de la nouvelle tête
      snake.unshift(newHead);

      // Collision avec soi-même
      for (let i = 1; i < snake.length; i++) {
        if (newHead.x === snake[i].x && newHead.y === snake[i].y) {
          gameOver = true;
          break;
        }
      }

      drawGame();

      if (gameOver) {
        gameOverScreen();
      }
    }

    // Dessiner le jeu sur le canvas
    function drawGame() {
      // Dessiner le fond
      ctx.fillStyle = WHITE;
      ctx.fillRect(0, 0, WIDTH, HEIGHT);

      // Dessiner le serpent
      ctx.fillStyle = GREEN;
      snake.forEach(segment => {
        ctx.fillRect(segment.x * GRID_SIZE, segment.y * GRID_SIZE, GRID_SIZE, GRID_SIZE);
      });

      // Dessiner la nourriture
      ctx.fillStyle = RED;
      ctx.fillRect(food.x * GRID_SIZE, food.y * GRID_SIZE, GRID_SIZE, GRID_SIZE);

      // Afficher le score
      ctx.fillStyle = "black";
      ctx.font = "20px sans-serif";
      ctx.fillText("Score: " + score, 10, 20);
    }

    // Afficher l'écran de fin
    function gameOverScreen() {
      ctx.fillStyle = RED;
      ctx.font = "40px sans-serif";
      const text = "Game Over!";
      const textWidth = ctx.measureText(text).width;
      ctx.fillText(text, (WIDTH - textWidth) / 2, HEIGHT / 2);
      clearInterval(gameInterval);
    }

    // Boucle de jeu : environ 10 mises à jour par seconde
    const gameInterval = setInterval(update, 100);
  </script>
</body>
</html>
