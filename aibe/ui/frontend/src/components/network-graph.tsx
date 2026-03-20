"use client";

import { useRef, useEffect, useState } from "react";
import dynamic from "next/dynamic";

const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), {
  ssr: false,
});



export default function NetworkGraph() {
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      const { clientWidth, clientHeight } = containerRef.current;
      setDimensions({ width: clientWidth, height: clientHeight });
    }
    
    const handleResize = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight,
        });
      }
    };
    
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const data = {
    nodes: [
      { id: "Oracle", group: 0, val: 20 },
      { id: "Minerva", group: 0, val: 15 },
      { id: "Scout", group: 1, val: 10 },
      { id: "Vega", group: 1, val: 10 },
      { id: "Pulse", group: 1, val: 10 },
      { id: "Forge", group: 2, val: 15 },
      { id: "Ember", group: 2, val: 10 },
      { id: "Flint", group: 2, val: 10 },
      { id: "Cinder", group: 2, val: 10 },
      { id: "Patch", group: 2, val: 8 },
      { id: "Deploy", group: 2, val: 12 },
    ],
    links: [
      { source: "Oracle", target: "Minerva" },
      { source: "Minerva", target: "Scout" },
      { source: "Scout", target: "Vega" },
      { source: "Scout", target: "Pulse" },
      { source: "Minerva", target: "Forge" },
      { source: "Forge", target: "Ember" },
      { source: "Forge", target: "Flint" },
      { source: "Flint", target: "Cinder" },
      { source: "Forge", target: "Patch" },
      { source: "Forge", target: "Deploy" },
      { source: "Pulse", target: "Oracle" },
    ]
  };

  const getGroupColor = (group: number) => {
    switch(group) {
      case 0: return "hsl(var(--primary))";
      case 1: return "hsl(var(--accent))";
      case 2: return "hsl(var(--secondary))";
      default: return "#52525b";
    }
  };

  return (
    <div ref={containerRef} className="w-full h-full">
      {dimensions.width > 0 && (
        <ForceGraph2D
          width={dimensions.width}
          height={dimensions.height}
          graphData={data}
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          nodeColor={(node: any) => getGroupColor(node.group)}
          nodeRelSize={4}
          linkColor={() => "rgba(255,255,255,0.2)"}
          linkWidth={1}
          linkDirectionalParticles={2}
          linkDirectionalParticleSpeed={0.01}
          linkDirectionalParticleWidth={2}
          backgroundColor="transparent"
        />
      )}
    </div>
  );
}
