/*
 * Standalone Console Flood Game
 * Simplified version that compiles without external dependencies
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_SIZE 20
#define MAX_COLORS 10

typedef struct {
    int w, h;
    int colors;
    int moves;
    int movelimit;
    char grid[MAX_SIZE * MAX_SIZE];
} GameState;

/* Fill a region with a new color */
void flood_fill(GameState *state, int x, int y, char oldcolor, char newcolor) {
    int w = state->w;
    int h = state->h;

    if (x < 0 || x >= w || y < 0 || y >= h)
        return;
    if (state->grid[y * w + x] != oldcolor)
        return;
    if (oldcolor == newcolor)
        return;

    state->grid[y * w + x] = newcolor;

    /* Recursively fill adjacent cells */
    flood_fill(state, x + 1, y, oldcolor, newcolor);
    flood_fill(state, x - 1, y, oldcolor, newcolor);
    flood_fill(state, x, y + 1, oldcolor, newcolor);
    flood_fill(state, x, y - 1, oldcolor, newcolor);
}

/* Check if the puzzle is complete */
int is_complete(GameState *state) {
    int wh = state->w * state->h;
    char first = state->grid[0];

    for (int i = 1; i < wh; i++) {
        if (state->grid[i] != first)
            return 0;
    }
    return 1;
}

/* Initialize a new game */
void init_game(GameState *state, int w, int h, int colors) {
    state->w = w;
    state->h = h;
    state->colors = colors;
    state->moves = 0;
    state->movelimit = (w * h) / 3 + 5; /* Rough estimate */

    /* Generate random grid */
    srand(time(NULL));
    for (int i = 0; i < w * h; i++) {
        state->grid[i] = '0' + (rand() % colors);
    }
}

/* Display the grid */
void display_grid(GameState *state) {
    printf("\n");
    for (int y = 0; y < state->h; y++) {
        printf("  ");
        for (int x = 0; x < state->w; x++) {
            printf("%c ", state->grid[y * state->w + x]);
        }
        printf("\n");
    }
    printf("\n  Moves: %d / %d\n", state->moves, state->movelimit);
}

/* Display color legend */
void display_colors(int colors) {
    printf("\n  Available colors: ");
    for (int i = 0; i < colors; i++) {
        printf("%c ", '0' + i);
    }
    printf("\n");
}

int main() {
    GameState game;
    char input[10];
    int color;

    printf("========================================\n");
    printf("        FLOOD PUZZLE GAME\n");
    printf("========================================\n");
    printf("Fill the entire grid with one color!\n");
    printf("Start from the top-left corner.\n");
    printf("========================================\n\n");

    /* Get game parameters */
    int w, h, colors;
    printf("Enter grid width (4-20): ");
    scanf("%d", &w);
    printf("Enter grid height (4-20): ");
    scanf("%d", &h);
    printf("Enter number of colors (3-9): ");
    scanf("%d", &colors);

    /* Validate input */
    if (w < 4 || w > 20) w = 12;
    if (h < 4 || h > 20) h = 12;
    if (colors < 3 || colors > 9) colors = 6;

    /* Initialize game */
    init_game(&game, w, h, colors);

    printf("\nGame initialized: %dx%d grid with %d colors\n", w, h, colors);

    /* Main game loop */
    while (!is_complete(&game) && game.moves < game.movelimit) {
        display_grid(&game);
        display_colors(game.colors);

        printf("\nEnter color to fill (0-%d), or 'q' to quit: ", game.colors - 1);
        scanf("%s", input);

        if (input[0] == 'q' || input[0] == 'Q') {
            printf("\nThanks for playing!\n");
            return 0;
        }

        color = input[0] - '0';

        if (color >= 0 && color < game.colors) {
            char current = game.grid[0];
            if (current != color + '0') {
                flood_fill(&game, 0, 0, current, color + '0');
                game.moves++;
            } else {
                printf("That's already the current color!\n");
            }
        } else {
            printf("Invalid color! Please choose 0-%d\n", game.colors - 1);
        }
    }

    /* Game over */
    display_grid(&game);

    if (is_complete(&game)) {
        printf("\n========================================\n");
        printf("   CONGRATULATIONS! YOU WON!\n");
        printf("   Completed in %d moves!\n", game.moves);
        printf("========================================\n");
    } else {
        printf("\n========================================\n");
        printf("   GAME OVER - Move limit reached\n");
        printf("   You used %d moves\n", game.moves);
        printf("========================================\n");
    }

    return 0;
}
