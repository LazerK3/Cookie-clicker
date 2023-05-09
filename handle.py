def find_window(keyword):
    import win32gui
    """Find a window containing the specified keyword in its name."""
    handle = None
    
    def enum_callback(hwnd, results):
        """Callback function for EnumWindows."""
        if keyword in win32gui.GetWindowText(hwnd):
            results.append(hwnd)

    results = []
    win32gui.EnumWindows(enum_callback, results)
    
    if results:
        handle = results[0]
    
    return handle

if __name__ == "__main__":
    print(find_window(input("Enter window keyword: ")))