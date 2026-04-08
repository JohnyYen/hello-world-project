"use client"

import * as React from "react"
import {
  closestCenter,
  DndContext,
  KeyboardSensor,
  MouseSensor,
  TouchSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
} from "@dnd-kit/core"
import { restrictToVerticalAxis } from "@dnd-kit/modifiers"
import {
  arrayMove,
  SortableContext,
  useSortable,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable"
import { CSS } from "@dnd-kit/utilities"
import {
  IconChevronDown,
  IconChevronLeft,
  IconChevronRight,
  IconChevronsLeft,
  IconChevronsRight,
  IconCircleCheckFilled,
  IconCircleDot,
  IconCircleX,
  IconDotsVertical,
  IconGripVertical,
  IconLayoutColumns,
  IconLoader,
  IconPlus,
  IconSearch,
  IconTrendingUp,
  IconFilter,
  IconX,
} from "@tabler/icons-react"
import {
  ColumnDef,
  ColumnFiltersState,
  flexRender,
  getCoreRowModel,
  getFacetedRowModel,
  getFacetedUniqueValues,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  Row,
  SortingState,
  useReactTable,
  VisibilityState,
} from "@tanstack/react-table"
import { toast } from "sonner"
import { z } from "zod"

import { useIsMobile } from "@/hooks/use-mobile"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Skeleton } from "@/components/ui/skeleton"
import { LevelPerformanceItem } from "@/types/api"

// Schema for level performance data from API
export const schema = z.object({
  levelName: z.string(),
  completionRate: z.number(),
  averageAttempts: z.number(),
  averageTimeMinutes: z.number(),
})

// Status configuration for styling
const statusConfig: Record<string, { label: string; color: string; bg: string; icon: React.ReactNode }> = {
  "published": { 
    label: "Publicado", 
    color: "text-emerald-600 dark:text-emerald-400", 
    bg: "bg-emerald-500/10 border-emerald-500/20",
    icon: <IconCircleCheckFilled className="w-3 h-3 fill-current" />
  },
  "draft": { 
    label: "Borrador", 
    color: "text-amber-600 dark:text-amber-400", 
    bg: "bg-amber-500/10 border-amber-500/20",
    icon: <IconLoader className="w-3 h-3 animate-spin" />
  },
  "archived": { 
    label: "Archivado", 
    color: "text-slate-500 dark:text-slate-400", 
    bg: "bg-slate-500/10 border-slate-500/20",
    icon: <IconCircleX className="w-3 h-3" />
  },
}

// Category configuration
const categoryColors: Record<string, string> = {
  "algorithm": "bg-violet-500/10 text-violet-600 dark:text-violet-400 border-violet-500/20",
  "logic": "bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/20",
  "syntax": "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20",
  "debugging": "bg-red-500/10 text-red-600 dark:text-red-400 border-red-500/20",
  "game": "bg-orange-500/10 text-orange-600 dark:text-orange-400 border-orange-500/20",
}

// Create a separate component for the drag handle
function DragHandle({ id }: { id: string }) {
  const { attributes, listeners } = useSortable({
    id,
  })

  return (
    <Button
      {...attributes}
      {...listeners}
      variant="ghost"
      size="icon"
      className="text-muted-foreground/50 hover:text-muted-foreground hover:bg-transparent size-7 cursor-grab active:cursor-grabbing transition-colors"
    >
      <IconGripVertical className="size-3.5" />
      <span className="sr-only">Drag to reorder</span>
    </Button>
  )
}

const columns: ColumnDef<z.infer<typeof schema>>[] = [
  {
    id: "drag",
    header: () => null,
    cell: ({ row }) => <DragHandle id={row.original.levelName} />,
    size: 40,
  },
  {
    id: "select",
    header: ({ table }) => (
      <div className="flex items-center justify-center">
        <Checkbox
          checked={
            table.getIsAllPageRowsSelected() ||
            (table.getIsSomePageRowsSelected() && "indeterminate")
          }
          onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
          aria-label="Seleccionar todo"
        />
      </div>
    ),
    cell: ({ row }) => (
      <div className="flex items-center justify-center">
        <Checkbox
          checked={row.getIsSelected()}
          onCheckedChange={(value) => row.toggleSelected(!!value)}
          aria-label="Seleccionar fila"
        />
      </div>
    ),
    enableSorting: false,
    enableHiding: false,
    size: 40,
  },
  {
    accessorKey: "levelName",
    header: "Nivel",
    cell: ({ row }) => {
      return <TableCellViewer item={row.original} />
    },
    enableHiding: false,
  },
  {
    accessorKey: "completionRate",
    header: "Tasa de Completado",
    cell: ({ row }) => {
      const rate = row.original.completionRate
      const rateColor = rate >= 80 ? "text-emerald-600 dark:text-emerald-400" : rate >= 50 ? "text-amber-600 dark:text-amber-400" : "text-red-600 dark:text-red-400"
      return (
        <div className="flex items-center gap-2">
          <div className="w-16 h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
            <div 
              className={`h-full ${rate >= 80 ? 'bg-emerald-500' : rate >= 50 ? 'bg-amber-500' : 'bg-red-500'}`}
              style={{ width: `${Math.min(rate, 100)}%` }}
            />
          </div>
          <span className={`font-semibold ${rateColor}`}>{rate.toFixed(0)}%</span>
        </div>
      )
    },
    filterFn: "includesString",
  },
  {
    accessorKey: "averageAttempts",
    header: "Intentos Promedio",
    cell: ({ row }) => (
      <div className="text-center font-mono text-sm">
        <span className="text-indigo-600 dark:text-indigo-400 font-semibold">{row.original.averageAttempts.toFixed(1)}</span>
      </div>
    ),
  },
  {
    accessorKey: "averageTimeMinutes",
    header: "Tiempo Promedio",
    cell: ({ row }) => {
      const time = row.original.averageTimeMinutes
      const formattedTime = time >= 60 
        ? `${Math.floor(time / 60)}h ${Math.round(time % 60)}m`
        : `${Math.round(time)}m`
      return (
        <div className="font-mono text-sm">
          <span className="text-slate-700 dark:text-slate-300">{formattedTime}</span>
        </div>
      )
    },
  },
  {
    id: "actions",
    cell: () => (
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            className="data-[state=open]:bg-muted text-muted-foreground flex size-8 hover:bg-indigo-500/10 hover:text-indigo-600"
            size="icon"
          >
            <IconDotsVertical />
            <span className="sr-only">Abrir menú</span>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-40 rounded-xl border-slate-200/60 dark:border-slate-800/60">
          <DropdownMenuItem className="rounded-lg">Ver Detalles</DropdownMenuItem>
          <DropdownMenuItem className="rounded-lg">Ver Estudiantes</DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem variant="destructive" className="rounded-lg">Archivar</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    ),
    size: 50,
  },
]

function DraggableRow({ row }: { row: Row<z.infer<typeof schema>> }) {
  const { transform, transition, setNodeRef, isDragging } = useSortable({
    id: row.original.levelName,
  })

  return (
    <TableRow
      data-state={row.getIsSelected() && "selected"}
      data-dragging={isDragging}
      ref={setNodeRef}
      className="relative z-0 data-[dragging=true]:z-10 data-[dragging=true]:opacity-80 group/row hover:bg-indigo-500/[0.02] dark:hover:bg-indigo-500/[0.05] transition-colors"
      style={{
        transform: CSS.Transform.toString(transform),
        transition: transition,
      }}
    >
      {row.getVisibleCells().map((cell) => (
        <TableCell key={cell.id} className="py-3">
          {flexRender(cell.column.columnDef.cell, cell.getContext())}
        </TableCell>
      ))}
    </TableRow>
  )
}

export function DataTable({
  data,
  isLoading = false,
  error = null,
}: {
  data: LevelPerformanceItem[]
  isLoading?: boolean
  error?: string | null
}) {
  const [rowSelection, setRowSelection] = React.useState({})
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({})
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  )
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [globalFilter, setGlobalFilter] = React.useState("")
  const [pagination, setPagination] = React.useState({
    pageIndex: 0,
    pageSize: 10,
  })
  const sortableId = React.useId()
  const sensors = useSensors(
    useSensor(MouseSensor, {}),
    useSensor(TouchSensor, {}),
    useSensor(KeyboardSensor, {})
  )

  const dataIds = data?.map(({ levelName }) => levelName) || []

  const table = useReactTable({
    data: data || [],
    columns,
    state: {
      sorting,
      columnVisibility,
      rowSelection,
      columnFilters,
      pagination,
      globalFilter,
    },
    getRowId: (row) => row.levelName,
    enableRowSelection: true,
    onRowSelectionChange: setRowSelection,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onColumnVisibilityChange: setColumnVisibility,
    onPaginationChange: setPagination,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
  })

  function handleDragEnd(event: DragEndEvent) {
    // Drag disabled for API data - read-only
  }

  // Loading state
  if (isLoading) {
    return (
      <div className="w-full flex flex-col gap-6 p-4 lg:p-6">
        <div className="flex items-center gap-3">
          <h2 className="text-xl font-semibold text-slate-800 dark:text-slate-200">
            Rendimiento por Nivel
          </h2>
        </div>
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="flex items-center gap-4 p-4 rounded-lg border border-slate-200/60 dark:border-slate-800/60">
              <Skeleton className="h-8 w-8 rounded" />
              <div className="flex-1 space-y-2">
                <Skeleton className="h-4 w-48" />
                <Skeleton className="h-2 w-full" />
              </div>
              <Skeleton className="h-4 w-16" />
              <Skeleton className="h-4 w-16" />
            </div>
          ))}
        </div>
      </div>
    )
  }

  // Error state - show empty table with error banner
  const showError = !!error

  return (
    <div className="w-full flex flex-col gap-6 p-4 lg:p-6">
      {/* Error Banner */}
      {showError && (
        <div className="rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-3">
          <p className="text-sm text-red-600 dark:text-red-400 flex items-center gap-2">
            <IconCircleX className="size-4" />
            Error al cargar los datos: {error}
          </p>
        </div>
      )}

      {/* Header Section with Search and Filters */}
      <div className="flex flex-col lg:flex-row gap-4 items-start lg:items-center justify-between">
        <div className="flex items-center gap-3">
          <h2 className="text-xl font-semibold text-slate-800 dark:text-slate-200">
            Rendimiento por Nivel
          </h2>
          <Badge variant="secondary" className="rounded-full px-3">
            {table.getFilteredRowModel().rows.length} niveles
          </Badge>
        </div>
        
        <div className="flex flex-wrap gap-3 items-center w-full lg:w-auto">
          {/* Search Input */}
          <div className="relative flex-1 lg:flex-initial">
            <IconSearch className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Buscar niveles..."
              value={globalFilter ?? ""}
              onChange={(event) => setGlobalFilter(event.target.value)}
              className="pl-9 w-full lg:w-64 rounded-lg border-slate-200/60 dark:border-slate-800/60 bg-white/50 dark:bg-slate-900/50"
            />
            {globalFilter && (
              <Button
                variant="ghost"
                size="icon"
                className="absolute right-1 top-1/2 -translate-y-1/2 h-6 w-6 hover:bg-transparent"
                onClick={() => setGlobalFilter("")}
              >
                <IconX className="w-3 h-3" />
              </Button>
            )}
          </div>

          {/* Completion Rate Filter */}
          <Select
            value={(table.getColumn("completionRate")?.getFilterValue() as string) ?? "all"}
            onValueChange={(value) => {
              table.getColumn("completionRate")?.setFilterValue(value === "all" ? undefined : value)
            }}
          >
            <SelectTrigger className="w-48 rounded-lg border-slate-200/60 dark:border-slate-800/60 bg-white/50 dark:bg-slate-900/50">
              <IconFilter className="w-4 h-4 mr-2" />
              <SelectValue placeholder="Filtrar por tasa" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todas las tasas</SelectItem>
              <SelectItem value="high">Alta (&gt;80%)</SelectItem>
              <SelectItem value="medium">Media (50-80%)</SelectItem>
              <SelectItem value="low">Baja (&lt;50%)</SelectItem>
            </SelectContent>
          </Select>

          {/* Columns Dropdown */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm" className="rounded-lg">
                <IconLayoutColumns className="w-4 h-4 mr-2" />
                <span className="hidden lg:inline">Columnas</span>
                <IconChevronDown className="w-4 h-4 ml-2" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56 rounded-xl border-slate-200/60 dark:border-slate-800/60">
              {table
                .getAllColumns()
                .filter(
                  (column) =>
                    typeof column.accessorFn !== "undefined" &&
                    column.getCanHide()
                )
                .map((column) => {
                  return (
                    <DropdownMenuCheckboxItem
                      key={column.id}
                      className="capitalize rounded-lg"
                      checked={column.getIsVisible()}
                      onCheckedChange={(value) =>
                        column.toggleVisibility(!!value)
                      }
                    >
                      {column.id}
                    </DropdownMenuCheckboxItem>
                  )
                })}
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Add Button */}
          <Button variant="outline" size="sm" className="rounded-lg border-indigo-500/30 text-indigo-600 hover:bg-indigo-500/10">
            <IconPlus className="w-4 h-4 mr-2" />
            <span className="hidden lg:inline">Agregar</span>
          </Button>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-hidden rounded-xl border border-slate-200/60 dark:border-slate-800/60 bg-white/50 dark:bg-slate-900/50">
        <DndContext
          collisionDetection={closestCenter}
          modifiers={[restrictToVerticalAxis]}
          onDragEnd={handleDragEnd}
          sensors={sensors}
          id={sortableId}
        >
          <Table>
            <TableHeader className="bg-slate-50/80 dark:bg-slate-900/80">
              {table.getHeaderGroups().map((headerGroup) => (
                <TableRow key={headerGroup.id} className="hover:bg-transparent border-slate-200/60 dark:border-slate-800/60">
                  {headerGroup.headers.map((header) => {
                    return (
                      <TableHead 
                        key={header.id} 
                        colSpan={header.colSpan}
                        className="text-slate-600 dark:text-slate-400 font-semibold text-xs uppercase tracking-wider"
                      >
                        {header.isPlaceholder
                          ? null
                          : flexRender(
                              header.column.columnDef.header,
                              header.getContext()
                            )}
                      </TableHead>
                    )
                  })}
                </TableRow>
              ))}
            </TableHeader>
            <TableBody className="divide-y divide-slate-100 dark:divide-slate-800/50">
              {table.getRowModel().rows?.length ? (
                <SortableContext
                  items={dataIds}
                  strategy={verticalListSortingStrategy}
                >
                  {table.getRowModel().rows.map((row) => (
                    <DraggableRow key={row.id} row={row} />
                  ))}
                </SortableContext>
              ) : (
                <TableRow>
                  <TableCell
                    colSpan={columns.length}
                    className="h-24 text-center text-muted-foreground"
                  >
                    No se encontraron resultados.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </DndContext>
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between px-2">
        <div className="text-sm text-muted-foreground hidden md:block">
          {table.getFilteredSelectedRowModel().rows.length} de{" "}
          {table.getFilteredRowModel().rows.length} fila(s) seleccionada(s).
        </div>
        <div className="flex items-center gap-4">
          <div className="hidden items-center gap-2 md:flex">
            <span className="text-sm font-medium text-slate-600 dark:text-slate-400">
              Filas por página
            </span>
            <Select
              value={`${table.getState().pagination.pageSize}`}
              onValueChange={(value) => {
                table.setPageSize(Number(value))
              }}
            >
              <SelectTrigger size="sm" className="w-20" id="rows-per-page">
                <SelectValue
                  placeholder={table.getState().pagination.pageSize}
                />
              </SelectTrigger>
              <SelectContent side="top">
                {[10, 20, 30, 40, 50].map((pageSize) => (
                  <SelectItem key={pageSize} value={`${pageSize}`}>
                    {pageSize}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="flex w-fit items-center justify-center text-sm font-medium">
            Página {table.getState().pagination.pageIndex + 1} de{" "}
            {table.getPageCount()}
          </div>
          <div className="flex items-center gap-1">
            <Button
              variant="outline"
              className="hidden h-8 w-8 p-0 lg:flex rounded-lg"
              onClick={() => table.setPageIndex(0)}
              disabled={!table.getCanPreviousPage()}
            >
              <span className="sr-only">Ir a primera página</span>
              <IconChevronsLeft className="w-4 h-4" />
            </Button>
            <Button
              variant="outline"
              className="size-8 rounded-lg"
              size="icon"
              onClick={() => table.previousPage()}
              disabled={!table.getCanPreviousPage()}
            >
              <span className="sr-only">Ir a página anterior</span>
              <IconChevronLeft className="w-4 h-4" />
            </Button>
            <Button
              variant="outline"
              className="size-8 rounded-lg"
              size="icon"
              onClick={() => table.nextPage()}
              disabled={!table.getCanNextPage()}
            >
              <span className="sr-only">Ir a siguiente página</span>
              <IconChevronRight className="w-4 h-4" />
            </Button>
            <Button
              variant="outline"
              className="hidden size-8 lg:flex rounded-lg"
              size="icon"
              onClick={() => table.setPageIndex(table.getPageCount() - 1)}
              disabled={!table.getCanNextPage()}
            >
              <span className="sr-only">Ir a última página</span>
              <IconChevronsRight className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

function TableCellViewer({ item }: { item: z.infer<typeof schema> }) {
  const isMobile = useIsMobile()

  return (
    <Drawer direction={isMobile ? "bottom" : "right"}>
      <DrawerTrigger asChild>
        <Button variant="link" className="text-foreground w-fit px-0 text-left">
          {item.levelName}
        </Button>
      </DrawerTrigger>
      <DrawerContent>
        <DrawerHeader className="gap-1">
          <DrawerTitle>{item.levelName}</DrawerTitle>
          <DrawerDescription>
            Rendimiento del nivel
          </DrawerDescription>
        </DrawerHeader>
        <div className="flex flex-col gap-4 overflow-y-auto px-4 text-sm">
          {!isMobile && (
            <>
              <Separator />
              <div className="grid gap-2">
                <div className="flex gap-2 leading-none font-medium">
                  Estadísticas del nivel
                  <IconTrendingUp className="size-4" />
                </div>
                <div className="text-muted-foreground">
                  Este nivel ha sido completado por el {item.completionRate.toFixed(0)}% de los estudiantes. 
                  El tiempo promedio de finalización es de {item.averageTimeMinutes.toFixed(0)} minutos 
                  con un promedio de {item.averageAttempts.toFixed(1)} intentos.
                </div>
              </div>
              <Separator />
            </>
          )}
          <form className="flex flex-col gap-4">
            <div className="flex flex-col gap-3">
              <Label htmlFor="levelName">Nombre del Nivel</Label>
              <Input id="levelName" defaultValue={item.levelName} />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-3">
                <Label htmlFor="completionRate">Tasa de Completado (%)</Label>
                <Input id="completionRate" type="number" defaultValue={item.completionRate} />
              </div>
              <div className="flex flex-col gap-3">
                <Label htmlFor="averageAttempts">Intentos Promedio</Label>
                <Input id="averageAttempts" type="number" step="0.1" defaultValue={item.averageAttempts} />
              </div>
            </div>
            <div className="flex flex-col gap-3">
              <Label htmlFor="averageTimeMinutes">Tiempo Promedio (minutos)</Label>
              <Input id="averageTimeMinutes" type="number" step="0.1" defaultValue={item.averageTimeMinutes} />
            </div>
          </form>
        </div>
        <DrawerFooter>
          <Button>Guardar Cambios</Button>
          <DrawerClose asChild>
            <Button variant="outline">Cerrar</Button>
          </DrawerClose>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  )
}
