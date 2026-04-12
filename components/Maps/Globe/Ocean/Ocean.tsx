export function Ocean(){
    return(
        <mesh renderOrder={1}>
            <sphereGeometry args={[100, 128, 128]} />
            <meshBasicMaterial color="#001638" transparent={false} opacity={1} />
        </mesh>
    )
}