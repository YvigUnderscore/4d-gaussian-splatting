import numpy as np
import argparse
import os

def generate_pose_bounds(self):
    try:
        # Chemin vers les fichiers COLMAP
        sparse_dir = filedialog.askdirectory(title="Sélectionnez le dossier sparse de COLMAP")
        if not sparse_dir:
            return

        output_file = filedialog.asksaveasfilename(
            defaultextension=".npy",
            filetypes=[("Fichiers Numpy", "*.npy")],
            title="Sauvegarder le fichier pose_bounds.npy"
        )
        if not output_file:
            return

        # Script de conversion des fichiers COLMAP en pose_bounds.npy
        command = [
            "python", "scripts/colmap_to_pose_bounds.py",
            "--input_dir", sparse_dir,
            "--output_file", output_file
        ]
        subprocess.run(command, check=True)
        messagebox.showinfo("Succès", f"Fichier pose_bounds.npy généré avec succès !\nChemin : {output_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Erreur lors de la génération : {e}")


def main():
    parser = argparse.ArgumentParser(description="Génère un fichier pose_bounds.npy pour un nombre donné de caméras.")
    parser.add_argument('--num_cameras', type=int, required=True, help="Nombre de caméras.")
    parser.add_argument('--output_file', type=str, required=True, help="Chemin du fichier pose_bounds.npy.")

    args = parser.parse_args()

    # Validation des entrées
    if args.num_cameras <= 0:
        print("Le nombre de caméras doit être supérieur à 0.")
        return

    # Création du répertoire de sortie si nécessaire
    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Générer les poses et les bounds
    generate_pose_bounds(args.num_cameras, args.output_file)

if __name__ == '__main__':
    main()
