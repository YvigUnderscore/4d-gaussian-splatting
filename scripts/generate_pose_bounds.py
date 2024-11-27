import argparse
import os
import numpy as np

def generate_pose_bounds(sparse_dir, output_file):
    """
    Génère le fichier pose_bounds.npy à partir des données sparses COLMAP.
    :param sparse_dir: Chemin vers le dossier contenant les fichiers sparses (cameras.txt, images.txt, points3D.txt).
    :param output_file: Chemin de sauvegarde pour le fichier pose_bounds.npy.
    """
    # Chemins des fichiers nécessaires
    cameras_file = os.path.join(sparse_dir, "cameras.txt")
    images_file = os.path.join(sparse_dir, "images.txt")
    points3D_file = os.path.join(sparse_dir, "points3D.txt")

    # Vérification des fichiers
    if not (os.path.exists(cameras_file) and os.path.exists(images_file) and os.path.exists(points3D_file)):
        raise FileNotFoundError("Les fichiers nécessaires (cameras.txt, images.txt, points3D.txt) sont introuvables dans le dossier sparse.")

    # Lecture des fichiers sparses
    poses = []
    with open(images_file, 'r') as f:
        for line in f:
            if line.startswith('#') or len(line.strip()) == 0:
                continue
            parts = line.split()
            qw, qx, qy, qz = map(float, parts[1:5])  # Quaternion
            tx, ty, tz = map(float, parts[5:8])  # Translation
            pose = quaternion_to_matrix(qw, qx, qy, qz, tx, ty, tz)
            poses.append(pose)

    # Calcul des limites (near et far)
    points = []
    with open(points3D_file, 'r') as f:
        for line in f:
            if line.startswith('#') or len(line.strip()) == 0:
                continue
            x, y, z = map(float, line.split()[1:4])
            points.append([x, y, z])

    points = np.array(points)
    distances = np.linalg.norm(points, axis=1)
    bounds = [distances.min(), distances.max()]

    # Sauvegarde des données dans le fichier .npy
    np.save(output_file, {"poses": np.array(poses), "bounds": bounds})
    print(f"Fichier pose_bounds.npy généré avec succès dans {output_file}.")

def quaternion_to_matrix(qw, qx, qy, qz, tx, ty, tz):
    """Convertit un quaternion en une matrice de transformation 4x4."""
    rotation = np.array([
        [1 - 2*qy**2 - 2*qz**2, 2*qx*qy - 2*qz*qw, 2*qx*qz + 2*qy*qw],
        [2*qx*qy + 2*qz*qw, 1 - 2*qx**2 - 2*qz**2, 2*qy*qz - 2*qx*qw],
        [2*qx*qz - 2*qy*qw, 2*qy*qz + 2*qx*qw, 1 - 2*qx**2 - 2*qy**2]
    ])
    transform = np.eye(4)
    transform[:3, :3] = rotation
    transform[:3, 3] = [tx, ty, tz]
    return transform

def main():
    parser = argparse.ArgumentParser(description="Génère un fichier pose_bounds.npy à partir des données sparses COLMAP.")
    parser.add_argument('--sparse_dir', type=str, required=True, help="Chemin vers le dossier contenant les fichiers sparses.")
    parser.add_argument('--output_file', type=str, required=True, help="Chemin de sauvegarde pour le fichier pose_bounds.npy.")

    args = parser.parse_args()

    # Validation des entrées
    if not os.path.exists(args.sparse_dir):
        print(f"Erreur : Le dossier spécifié n'existe pas : {args.sparse_dir}")
        return

    # Générer le fichier pose_bounds.npy
    try:
        generate_pose_bounds(args.sparse_dir, args.output_file)
    except Exception as e:
        print(f"Erreur lors de la génération de pose_bounds.npy : {e}")

if __name__ == "__main__":
    main()

