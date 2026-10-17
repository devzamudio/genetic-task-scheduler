import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import type { ConvergenceData } from '../../types';

interface MultiConvergenceChartProps {
  data: ConvergenceData;
}

export function MultiConvergenceChart({ data }: MultiConvergenceChartProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || data.best.length === 0) return;

    const margin = { top: 20, right: 100, bottom: 40, left: 60 };
    const width = 900 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const maxGen = Math.max(data.best.length, data.worst.length, data.avg.length) - 1;
    const allValues = [...data.best, ...data.worst, ...data.avg];
    const yMin = d3.min(allValues) || 0;
    const yMax = d3.max(allValues) || 0;

    const xScale = d3.scaleLinear().domain([0, maxGen]).range([0, width]);
    const yScale = d3.scaleLinear().domain([yMin * 0.95, yMax * 1.05]).range([height, 0]);

    svg.append('g').attr('transform', `translate(0,${height})`).call(d3.axisBottom(xScale).ticks(10));
    svg.append('g').call(d3.axisLeft(yScale));

    svg.append('text').attr('x', width / 2).attr('y', height + 35).attr('fill', 'black').attr('text-anchor', 'middle').text('Generación');
    svg.append('text').attr('transform', 'rotate(-90)').attr('y', -45).attr('x', -height / 2).attr('fill', 'black').attr('text-anchor', 'middle').text('Makespan');

    const drawLine = (dataArr: number[], color: string) => {
      const line = d3.line<number>()
        .x((_, i) => xScale(i))
        .y(d => yScale(d))
        .defined(d => !isNaN(d));

      svg.append('path')
        .datum(dataArr)
        .attr('fill', 'none')
        .attr('stroke', color)
        .attr('stroke-width', 2)
        .attr('d', line);
    };

    drawLine(data.best, '#10b981');
    drawLine(data.worst, '#ef4444');
    drawLine(data.avg, '#3b82f6');

    const legend = svg.append('g').attr('transform', `translate(${width + 10}, 0)`);
    const legendData = [
      { label: 'Mejor', color: '#10b981' },
      { label: 'Peor', color: '#ef4444' },
      { label: 'Promedio', color: '#3b82f6' }
    ];

    legendData.forEach((d, i) => {
      const g = legend.append('g').attr('transform', `translate(0, ${i * 25})`);
      g.append('rect').attr('width', 12).attr('height', 12).attr('fill', d.color);
      g.append('text').attr('x', 18).attr('y', 10).attr('font-size', '12px').attr('fill', 'black').text(d.label);
    });

  }, [data]);

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Gráfica de Convergencia (20 Ejecuciones)
      </h2>
      <div className="overflow-x-auto flex justify-center">
        <svg ref={svgRef}></svg>
      </div>
    </div>
  );
}