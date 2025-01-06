# Shazam-like-app
## Description
<div align="justify"> This desktop app implements a simplified version of audio fingerprinting, similar to the technology used by music recognition apps like Shazam, to identify songs based on short audio samples. The project involves involves a small database of songs, each separated into music and vocal tracks, and generating spectrograms for the first 30 seconds of each audio file.  Key features are then extracted from these spectrograms, and perceptual hash functions are applied to generate condensed fingerprints. Given a new audio sample, the application generates its spectrogram and fingerprint, comparing these against the database to identify the closest matches using a similarity index, presented in a user-friendly PyQt5 GUI. The project also allows users to create a weighted average of two audio files and search for matches, demonstrating the robustness of the fingerprinting technique. </div>

## Demo Videos
### Music & Vocals of one Song
https://github.com/user-attachments/assets/bef494f0-34e4-4aba-89b8-ce4b8a9856ab
### Mixing Two Songs
https://github.com/user-attachments/assets/14295965-6a46-4429-be34-89d7bf08788f

## Different Scenarios
### Results When Uploading Vocals Only
When user uploads to vocal files (i.e. no instruments), the results do not include any instrument only files from the database.
![image](https://github.com/user-attachments/assets/85c430a9-4bd5-4fa5-8a0d-a2f59ca53f10)
### Results When Uploading Music Only
When user uploads files that don't contain any vocals, none of the results is a vocals-only file
![image](https://github.com/user-attachments/assets/a8c4d384-8236-43fd-a48d-088daebfdaa8)

## Team Members
<div align="center">
  <table style="border-collapse: collapse; border: none;">
    <tr>
      <td align="center" style="border: none;">
        <img src="https://github.com/user-attachments/assets/e8713727-6257-4c16-b9bd-8f6cb509cf1c" alt="Enjy Ashraf" width="150" height="150"><br>
        <a href="https://github.com/enjyashraf18"><b>Enjy Ashraf</b></a>
      </td>
      <td align="center" style="border: none;">
        <img src="https://github.com/user-attachments/assets/5de3e403-7fce-4000-95d2-e9f07e0d78cf" alt="Nada Khaled" width="150" height="150"><br>
        <a href="https://github.com/NadaKhaled157"><b>Nada Khaled</b></a>
      </td>
      <td align="center" style="border: none;">
        <img src="https://github.com/user-attachments/assets/4b1f5180-2250-49ae-869f-4d00fb89447a" alt="Habiba Alaa" width="150" height="150"><br>
        <a href="https://github.com/habibaalaa123"><b>Habiba Alaa</b></a>
      </td>
      <td align="center" style="border: none;">
        <img src="https://github.com/user-attachments/assets/567fd220-acc8-4094-bfe0-5939a0048ca9" alt="Shahd Ahmed" width="150" height="150"><br>
        <a href="https://github.com/Shahd-A-Mahmoud"><b>Shahd Ahmed</b></a>
      </td>
    </tr>
  </table>
</div>




