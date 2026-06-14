"use client";

import { cn } from "@/lib/utils";

interface GameOption {
  id: string | null;
  title: string;
}

interface GameSelectorProps {
  games: GameOption[];
  selectedGameId: string | null;
  onSelect: (gameId: string | null) => void;
  isLoading?: boolean;
}

export function GameSelector({
  games,
  selectedGameId,
  onSelect,
  isLoading,
}: GameSelectorProps) {
  if (isLoading) {
    return (
      <div className="flex items-center gap-3">
        <span className="text-sm font-medium text-muted-foreground">
          Cargando juegos...
        </span>
        <div className="flex gap-2">
          {[...Array(3)].map((_, i) => (
            <div
              key={i}
              className="h-9 w-24 rounded-full bg-slate-200 dark:bg-slate-800 animate-pulse"
            />
          ))}
        </div>
      </div>
    );
  }

  if (!games || games.length <= 1) {
    return null;
  }

  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className="text-sm font-medium text-muted-foreground mr-1">
        Juego:
      </span>
      <div className="flex flex-wrap gap-2">
        {games.map((game) => (
          <button
            key={game.id ?? "all"}
            onClick={() => onSelect(game.id)}
            className={cn(
              "relative px-4 py-2 rounded-full text-sm font-medium transition-all duration-200",
              "border border-slate-200 dark:border-slate-700",
              "hover:shadow-md hover:scale-105 active:scale-95",
              selectedGameId === game.id
                ? "bg-indigo-600 text-white border-indigo-600 shadow-lg shadow-indigo-200 dark:shadow-indigo-900/30"
                : "bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:border-indigo-300 dark:hover:border-indigo-600 hover:text-indigo-600 dark:hover:text-indigo-400",
            )}
          >
            {game.title}
            {selectedGameId === game.id && (
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-indigo-400 rounded-full border-2 border-white dark:border-slate-900" />
            )}
          </button>
        ))}
      </div>
    </div>
  );
}
