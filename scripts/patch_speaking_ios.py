from pathlib import Path

p = Path('src/EnglishLoop.tsx')
s = p.read_text(encoding='utf-8')

# Prefer Safari's current audio containers/codecs, but keep cross-browser fallbacks.
old_mime = '''function speakingMimeType() {\n  if (typeof MediaRecorder === "undefined" || typeof MediaRecorder.isTypeSupported !== "function") return "";\n  return ["audio/mp4", "audio/webm;codecs=opus", "audio/webm"].find((t) => MediaRecorder.isTypeSupported(t)) || "";\n}'''
new_mime = '''function speakingMimeType() {\n  if (typeof MediaRecorder === "undefined" || typeof MediaRecorder.isTypeSupported !== "function") return "";\n  return [\n    "audio/mp4;codecs=pcm",\n    "audio/mp4",\n    "audio/webm;codecs=opus",\n    "audio/webm",\n  ].find((t) => MediaRecorder.isTypeSupported(t)) || "";\n}'''
if old_mime in s:
    s = s.replace(old_mime, new_mime, 1)

old_start = '''  const start = async () => {\n    setError("");\n    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") {\n      setError("This browser cannot record audio. Open the demo in Safari 14.5 or later over HTTPS.");\n      return;\n    }\n    setPhase("requesting");\n    try {\n      const stream = await navigator.mediaDevices.getUserMedia({\n        audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true },\n      });\n      const mimeType = speakingMimeType();\n      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);\n      chunksRef.current = [];\n      streamRef.current = stream;\n      recorderRef.current = recorder;\n      recorder.ondataavailable = (event) => { if (event.data?.size) chunksRef.current.push(event.data); };\n      recorder.onerror = () => {\n        setError("The recording stopped unexpectedly. Please try again.");\n        setPhase("idle");\n        stream.getTracks().forEach((track) => track.stop());\n      };\n      recorder.onstop = () => {\n        const seconds = Math.max(1, Math.round((Date.now() - startRef.current) / 1000));\n        const blob = new Blob(chunksRef.current, { type: recorder.mimeType || mimeType || "audio/mp4" });\n        stream.getTracks().forEach((track) => track.stop());\n        streamRef.current = null;\n        if (!blob.size) {\n          setError("Safari did not return an audio file. Please record again.");\n          setPhase("idle");\n          return;\n        }\n        if (audioUrl) URL.revokeObjectURL(audioUrl);\n        blobRef.current = blob;\n        setSec(seconds);\n        setAudioUrl(URL.createObjectURL(blob));\n        setPhase("ready");\n      };\n      startRef.current = Date.now();\n      setSec(0);\n      recorder.start();\n      setPhase("recording");\n    } catch (err) {\n      const denied = err?.name === "NotAllowedError" || err?.name === "SecurityError";\n      setError(denied\n        ? "Microphone access was denied. Allow microphone access for this site in Safari settings, then tap Record again."\n        : "The microphone is unavailable. Check that no other app is using it and try again.");\n      setPhase("idle");\n    }\n  };'''

new_start = '''  const start = async () => {\n    setError("");\n    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") {\n      setError("Audio recording is not available in this browser. Open the HTTPS page in Safari and try again.");\n      return;\n    }\n    setPhase("requesting");\n    try {\n      // Keep the microphone constraint intentionally simple for iPhone Safari.\n      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });\n      const mimeType = speakingMimeType();\n      let recorder;\n      try {\n        recorder = mimeType ? new MediaRecorder(stream, { mimeType }) : new MediaRecorder(stream);\n      } catch {\n        // Some Safari builds report a type as supported but reject it in the constructor.\n        recorder = new MediaRecorder(stream);\n      }\n\n      chunksRef.current = [];\n      streamRef.current = stream;\n      recorderRef.current = recorder;\n      recorder.onstart = () => {\n        startRef.current = Date.now();\n        setSec(0);\n        setPhase("recording");\n      };\n      recorder.ondataavailable = (event) => {\n        if (event.data && event.data.size > 0) chunksRef.current.push(event.data);\n      };\n      recorder.onerror = (event) => {\n        setError(`Recording error${event?.error?.name ? `: ${event.error.name}` : ""}. Please try again.`);\n        setPhase("idle");\n        stream.getTracks().forEach((track) => track.stop());\n        streamRef.current = null;\n      };\n      recorder.onstop = () => {\n        const seconds = Math.max(1, Math.round((Date.now() - startRef.current) / 1000));\n        const firstChunkType = chunksRef.current.find((chunk) => chunk?.type)?.type || "";\n        const blobType = recorder.mimeType || firstChunkType || mimeType || "audio/mp4";\n        const blob = new Blob(chunksRef.current, { type: blobType });\n        stream.getTracks().forEach((track) => track.stop());\n        streamRef.current = null;\n        if (!blob.size) {\n          setError("No audio was captured. Tap Record and speak for a few seconds before stopping.");\n          setPhase("idle");\n          return;\n        }\n        if (audioUrl) URL.revokeObjectURL(audioUrl);\n        blobRef.current = blob;\n        setSec(seconds);\n        setAudioUrl(URL.createObjectURL(blob));\n        setPhase("ready");\n      };\n\n      // A timeslice makes Safari emit chunks during recording instead of relying on one final blob.\n      recorder.start(1000);\n    } catch (err) {\n      streamRef.current?.getTracks().forEach((track) => track.stop());\n      streamRef.current = null;\n      const name = err?.name || "";\n      const denied = name === "NotAllowedError" || name === "SecurityError";\n      setError(denied\n        ? "Microphone access was denied. Allow microphone access for this site, reload the page, then tap Record again."\n        : `Could not start the microphone${name ? ` (${name})` : ""}. Reload the page and try again.`);\n      setPhase("idle");\n    }\n  };'''

if old_start not in s:
    raise RuntimeError('Speaking start handler anchor not found')
s = s.replace(old_start, new_start, 1)

old_stop = '''  const stop = () => {\n    if (recorderRef.current?.state !== "recording") return;\n    setPhase("processing");\n    recorderRef.current.stop();\n  };'''
new_stop = '''  const stop = () => {\n    const recorder = recorderRef.current;\n    if (!recorder || recorder.state !== "recording") return;\n    setPhase("processing");\n    try { recorder.requestData?.(); } catch {}\n    // Give Safari one animation frame to flush the requested chunk before stop().\n    window.setTimeout(() => {\n      try {\n        if (recorder.state === "recording") recorder.stop();\n      } catch {\n        setError("Could not stop the recording cleanly. Please try again.");\n        setPhase("idle");\n      }\n    }, 60);\n  };'''
if old_stop not in s:
    raise RuntimeError('Speaking stop handler anchor not found')
s = s.replace(old_stop, new_stop, 1)

old_play = '''  const togglePlay = async () => {\n    if (!audioRef.current) return;\n    if (audioRef.current.paused) {\n      await audioRef.current.play();\n      setPlaying(true);\n    } else {\n      audioRef.current.pause();\n      setPlaying(false);\n    }\n  };'''
new_play = '''  const togglePlay = async () => {\n    if (!audioRef.current) return;\n    try {\n      if (audioRef.current.paused) {\n        await audioRef.current.play();\n        setPlaying(true);\n      } else {\n        audioRef.current.pause();\n        setPlaying(false);\n      }\n    } catch {\n      setPlaying(false);\n      setError("Safari could not play this recording. Re-record it and try again.");\n    }\n  };'''
if old_play in s:
    s = s.replace(old_play, new_play, 1)

# Expose native controls as a fallback on iPhone while keeping the custom play button.
old_audio = '''            <audio ref={audioRef} src={audioUrl} preload="metadata" playsInline\n              onEnded={() => setPlaying(false)} onPause={() => setPlaying(false)} onPlay={() => setPlaying(true)} />'''
new_audio = '''            <audio ref={audioRef} src={audioUrl} preload="metadata" playsInline controls\n              style={{ width: "100%", marginBottom: 12 }}\n              onEnded={() => setPlaying(false)} onPause={() => setPlaying(false)} onPlay={() => setPlaying(true)} />'''
if old_audio in s:
    s = s.replace(old_audio, new_audio, 1)

# Build-time safeguards: do not publish the old fragile recording path again.
for forbidden in [
    'audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true }',
    'recorder.start();\n      setPhase("recording")',
]:
    if forbidden in s:
        raise RuntimeError(f'Old fragile Speaking code remains: {forbidden}')

p.write_text(s, encoding='utf-8')
