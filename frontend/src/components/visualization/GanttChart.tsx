import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import type { GanttTask } from '../../types';

interface GanttChartProps {
  tasks: GanttTask[];
  machines: string[];
}

export function GanttChart({ tasks, machines }: GanttChartProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || tasks.length === 0) return;

    const margin = { top: 20, right: 30, bottom: 40, left: 80 };
    const width = 900 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Limpiar SVG anterior
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Escalas
    const xScale = d3.scaleLinear()
      .domain([0, d3.max(tasks, d => d.end_time) || 0])
      .range([0, width]);

    const yScale = d3.scaleBand()
      .domain(machines)
      .range([0, height])
      .padding(0.2);

    // Ejes
    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(xScale).ticks(10))
      .append('text')
      .attr('x', width / 2)
      .attr('y', 35)
      .attr('fill', 'black')
      .attr('text-anchor', 'middle')
      .text('Tiempo');

    svg.append('g')
      .call(d3.axisLeft(yScale))
      .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', -60)
      .attr('x', -height / 2)
      .attr('fill', 'black')
      .attr('text-anchor', 'middle')
      .text('Máquinas');

    // Colores por trabajo
    const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

    // Barras de Gantt
    svg.selectAll('.bar')
      .data(tasks)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', d => xScale(d.start_time))
      .attr('y', d => yScale(d.machine) || 0)
      .attr('width', d => xScale(d.end_time) - xScale(d.start_time))
      .attr('height', yScale.bandwidth())
      .attr('fill', d => colorScale(d.job_id.toString()))
      .attr('stroke', '#333')
      .attr('stroke-width', 1);

    // Etiquetas en las barras
    svg.selectAll('.label')
      .data(tasks)
      .enter()
      .append('text')
      .attr('class', 'label')
      .attr('x', d => xScale(d.start_time) + (xScale(d.end_time) - xScale(d.start_time)) / 2)
      .attr('y', d => (yScale(d.machine) || 0) + yScale.bandwidth() / 2)
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'middle')
      .attr('fill', 'white')
      .attr('font-size', '10px')
      .attr('font-weight', 'bold')
      .text(d => `J${d.job_id}-O${d.op_id}`);

  }, [tasks, machines]);

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Diagrama de Gantt
      </h2>
      <div className="overflow-x-auto">
        <svg ref={svgRef}></svg>
      </div>
    </div>
  );
}