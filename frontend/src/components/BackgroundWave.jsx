import { useEffect, useRef } from 'react';

export default function BackgroundWave() {
    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        let animationId;
        let time = 0;

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resize);
        resize();

        const animate = () => {
            time += 0.02;
            ctx.fillStyle = '#050505';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            for (let i = 0; i < 6; i++) {
                ctx.beginPath();
                ctx.strokeStyle = `rgba(212, 175, 55, ${0.15 + i * 0.05})`;
                ctx.lineWidth = 1;

                for (let x = 0; x < canvas.width; x += 5) {
                    const y = canvas.height / 2 +
                        Math.sin(x * 0.003 + time + i * 0.5) * 60 +
                        Math.sin(x * 0.01 - time * 0.5) * 30;

                    if (x === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }
                ctx.stroke();
            }

            animationId = requestAnimationFrame(animate);
        };

        animate();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, []);

    return <canvas ref={canvasRef} className="absolute inset-0 z-0" />;
}
