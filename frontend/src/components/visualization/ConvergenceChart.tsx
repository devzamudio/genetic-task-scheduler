import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface ConvergenceChartProps {
  convergence: number[];
}

export function ConvergenceChart({ convergence }: ConvergenceChartProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || convergence.length === 0) return;

    const margin = { top: 20, right: 30, bottom: 40, left: 60 };
    const width = 900 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const data = convergence.map((value, index) => ({ generation: index, makespan: value }));

    const xScale = d3.scaleLinear()
      .domain([0, data.length - 1])
      .range([0, width]);

    const yScale = d3.scaleLinear()
      .domain([d3.min(data, d => d.makespan) || 0, d3.max(data, d => d.makespan) || 0])
      .range([height, 0]);

    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(xScale).ticks(10))
      .append('text')
      .attr('x', width / 2)
      .attr('y', 35)
      .attr('fill', 'black')
      .attr('text-anchor', 'middle')
      .text('Generación');

    svg.append('g')
      .call(d3.axisLeft(yScale))
      .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', -45)
      .attr('x', -height / 2)
      .attr('fill', 'black')
      .attr('text-anchor', 'middle')
      .text('Makespan');

    const line = d3.line<{ generation: number; makespan: number }>()
      .x(d => xScale(d.generation))
      .y(d => yScale(d.makespan));

    svg.append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', '#0ea5e9')
      .attr('stroke-width', 2)
      .attr('d', line);

    svg.selectAll('.dot')
      .data(data)
      .enter()
      .append('circle')
      .attr('class', 'dot')
      .attr('cx', d => xScale(d.generation))
      .attr('cy', d => yScale(d.makespan))
      .attr('r', 3)
      .attr('fill', '#0ea5e9');

  }, [convergence]);

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Gráfica de Convergencia (Ejecución Única)
      </h2>
      <div className="overflow-x-auto">
        <svg ref={svgRef}></svg>
      </div>
    </div>
  );
}