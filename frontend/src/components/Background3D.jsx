import { Canvas } from '@react-three/fiber';
import { Stars } from '@react-three/drei';

export default function Background3D() {
    return (
        <div className="fixed inset-0 -z-10 transition-colors duration-1000" style={{ backgroundColor: '#0B0C15', zIndex: -1 }}>
            <Canvas camera={{ position: [0, 0, 1] }}>
                <Stars
                    radius={100}
                    depth={50}
                    count={5000}
                    factor={4}
                    saturation={0}
                    fade
                    speed={1}
                />
            </Canvas>
            {/* Ambient Gradient Overlay for depth */}
            <div className="absolute inset-0 bg-gradient-to-t from-midnight via-transparent to-transparent opacity-80 pointer-events-none" />
        </div>
    );
}
